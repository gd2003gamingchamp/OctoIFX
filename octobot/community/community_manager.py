#  gd2003gamingchamp OctoIFX
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import time
import asyncio
import json
import requests
import threading

import octobot_commons.logging as logging
import octobot_commons.config_manager as config_manager
import octobot_commons.os_util as os_util

import octobot_commons.constants as common_constants

import octobot_evaluators.api as evaluator_api
import octobot_evaluators.enums as evaluator_enums

import octobot_services.constants as service_constants

import octobot_trading.api as trading_api

import octobot.community.community_fields as community_fields


class CommunityManager:
    _headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self, octobot_api):
        self.octobot_api = octobot_api
        self.edited_config = octobot_api.get_edited_config()
        self.enabled = config_manager.get_metrics_enabled(self.edited_config)
        self.bot_id = self._init_config_bot_id(self.edited_config)
        self.reference_market = trading_api.get_reference_market(self.edited_config)
        self.logger = logging.get_logger(self.__class__.__name__)
        self.current_config = None
        self.keep_running = True
        self.session = octobot_api.get_aiohttp_session()

        # these attributes will be set at the last moment to ensure relevance and let time for everything to startup
        self.has_real_trader = None
        self.has_simulator = None
        self.exchange_managers = None

    def _init_community_config(self):
        self.has_real_trader = trading_api.is_trader_enabled_in_config(self.edited_config)
        self.has_simulator = trading_api.is_trader_simulator_enabled_in_config(self.edited_config)
        self.exchange_managers = trading_api.get_exchange_managers_from_exchange_ids(
            self.octobot_api.get_exchange_manager_ids())

    async def start_community_task(self):
        if self.enabled:
            try:
                # first ensure this session is not just a configuration test: register after a timer
                await asyncio.sleep(common_constants.TIMER_BEFORE_METRICS_REGISTRATION_SECONDS)
                self._init_community_config()
                await self.register_session()
                while self.keep_running:
                    # send a keepalive at periodic intervals
                    await asyncio.sleep(common_constants.TIMER_BETWEEN_METRICS_UPTIME_UPDATE)
                    try:
                        await self._update_uptime_and_profitability()
                    except Exception as e:
                        self.logger.debug(f"Exception when handling community data : {e}")
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.debug(f"Exception when handling community registration: {e}")

    async def stop_task(self):
        self.keep_running = False
        await self.session.close()

    @staticmethod
    def should_register_bot(config):
        existing_id = CommunityManager._init_config_bot_id(config)
        return not existing_id

    @staticmethod
    def background_get_id_and_register_bot(octobot_api):
        community_manager = CommunityManager(octobot_api)
        threading.Thread(target=community_manager._blocking_get_id_and_register).start()

    def _blocking_get_id_and_register(self):
        try:
            resp = requests.get(f"{common_constants.METRICS_URL}{common_constants.METRICS_ROUTE_GEN_BOT_ID}",
                                headers=self._headers)
            text = resp.text
            if resp.status_code != 200:
                self.logger.debug(f"Impossible to get bot id: status code: {resp.status_code}, text: {text}")
            else:
                self.bot_id = json.loads(text)
                self._save_bot_id()
                community = self._get_bot_community()
                requests.post(f"{common_constants.METRICS_URL}{common_constants.METRICS_ROUTE_REGISTER}",
                              json=community, headers=self._headers)
        except Exception as e:
            self.logger.debug(f"Error when handling community: {e}")

    @staticmethod
    def _init_config_bot_id(config):
        if common_constants.CONFIG_METRICS in config and config[common_constants.CONFIG_METRICS] and \
                common_constants.CONFIG_METRICS_BOT_ID in config[common_constants.CONFIG_METRICS]:
            return config[common_constants.CONFIG_METRICS][common_constants.CONFIG_METRICS_BOT_ID]
        else:
            return None

    async def register_session(self, retry_on_error=True):
        self.current_config = await self._get_current_community_config()
        await self._post_community_data(common_constants.METRICS_ROUTE_REGISTER, self.current_config, retry_on_error)

    async def _update_uptime_and_profitability(self, retry_on_error=True):
        self.current_config[community_fields.CommunityFields.CURRENT_SESSION.value][
            community_fields.CommunityFields.UP_TIME.value] = int(time.time() - self.octobot_api.get_start_time())
        self.current_config[community_fields.CommunityFields.CURRENT_SESSION.value][
            community_fields.CommunityFields.PROFITABILITY.value] = self._get_profitability()
        await self._post_community_data(common_constants.METRICS_ROUTE_UPTIME, self.current_config, retry_on_error)

    async def _get_current_community_config(self):
        if not self.bot_id:
            await self._init_bot_id()
        if self.bot_id:
            return self._get_bot_community()

    def _get_bot_community(self):
        return {
            community_fields.CommunityFields.ID.value: self.bot_id,
            community_fields.CommunityFields.CURRENT_SESSION.value: {
                community_fields.CommunityFields.STARTED_AT.value: int(self.octobot_api.get_start_time()),
                community_fields.CommunityFields.UP_TIME.value: int(time.time() - self.octobot_api.get_start_time()),
                community_fields.CommunityFields.SIMULATOR.value: self.has_simulator,
                community_fields.CommunityFields.TRADER.value: self.has_real_trader,
                community_fields.CommunityFields.EVAL_CONFIG.value: self._get_eval_config(),
                community_fields.CommunityFields.PAIRS.value: self._get_traded_pairs(),
                community_fields.CommunityFields.EXCHANGES.value: list(trading_api.get_exchange_names()),
                community_fields.CommunityFields.NOTIFICATIONS.value: self._get_notification_types(),
                community_fields.CommunityFields.TYPE.value: os_util.get_octobot_type(),
                community_fields.CommunityFields.PLATFORM.value: os_util.get_current_platform(),
                community_fields.CommunityFields.REFERENCE_MARKET.value: self.reference_market,
                community_fields.CommunityFields.PORTFOLIO_VALUE.value: self._get_real_portfolio_value(),
                community_fields.CommunityFields.PROFITABILITY.value: self._get_profitability()
            }
        }

    def _get_profitability(self):
        total_origin_values = 0
        total_profitability = 0

        for exchange_manager in self.exchange_managers:
            profitability, _, _, _, _ = trading_api.get_profitability_stats(exchange_manager)
            total_profitability += profitability
            total_origin_values += trading_api.get_current_portfolio_value(exchange_manager)

        return total_profitability * 100 / total_origin_values if total_origin_values > 0 else 0

    def _get_real_portfolio_value(self):
        if self.has_real_trader:
            total_value = 0
            for exchange_manager in self.exchange_managers:
                current_value = trading_api.get_current_portfolio_value(exchange_manager)
                # current_value might be 0 if no trades have been made / canceled => use origin value
                if current_value == 0:
                    current_value = trading_api.get_origin_portfolio_value(exchange_manager)
                total_value += current_value
            return total_value
        else:
            return 0

    def _get_traded_pairs(self):
        pairs = set()
        for exchange_manager in self.exchange_managers:
            pairs = pairs.union(trading_api.get_trading_pairs(exchange_manager))
        return list(pairs)

    def _get_notification_types(self):
        has_notifications = service_constants.CONFIG_CATEGORY_NOTIFICATION in self.edited_config \
                            and service_constants.CONFIG_NOTIFICATION_TYPE in self.edited_config[
                                service_constants.CONFIG_CATEGORY_NOTIFICATION]
        return self.edited_config[service_constants.CONFIG_CATEGORY_NOTIFICATION][
            service_constants.CONFIG_NOTIFICATION_TYPE] if has_notifications else []

    def _get_eval_config(self):
        tentacle_setup_config = self.octobot_api.get_tentacles_setup_config()
        # trading mode
        config_eval = []
        if (trading_mode := self.octobot_api.get_trading_mode()) is not None:
            config_eval.append(trading_mode.get_name())

        # strategies
        for strategy in evaluator_api.get_evaluator_classes_from_type(
                evaluator_enums.EvaluatorMatrixTypes.STRATEGIES.value,
                tentacle_setup_config):
            config_eval.append(strategy.get_name())

        # evaluators
        evaluators = evaluator_api.get_evaluator_classes_from_type(evaluator_enums.EvaluatorMatrixTypes.TA.value,
                                                                   tentacle_setup_config)
        evaluators += evaluator_api.get_evaluator_classes_from_type(evaluator_enums.EvaluatorMatrixTypes.SOCIAL.value,
                                                                    tentacle_setup_config)
        evaluators += evaluator_api.get_evaluator_classes_from_type(
            evaluator_enums.EvaluatorMatrixTypes.REAL_TIME.value,
            tentacle_setup_config)
        for evaluator in evaluators:
            config_eval.append(evaluator.get_name())
        return config_eval

    async def _init_bot_id(self):
        try:
            async with self.session.get(f"{common_constants.METRICS_URL}{common_constants.METRICS_ROUTE_GEN_BOT_ID}",
                                        headers=self._headers) as resp:
                text = await resp.text()
                if resp.status != 200:
                    self.logger.debug(f"Impossible to get bot id: status code: {resp.status}, text: {text}")
                else:
                    self.bot_id = json.loads(text)
                    self._save_bot_id()
        except Exception as e:
            self.logger.debug(f"Error when handling community data : {e}")

    def _save_bot_id(self):
        if common_constants.CONFIG_METRICS not in self.edited_config \
                or not self.edited_config[common_constants.CONFIG_METRICS]:
            self.edited_config[common_constants.CONFIG_METRICS] = {common_constants.CONFIG_ENABLED_OPTION: True}
        self.edited_config[common_constants.CONFIG_METRICS][common_constants.CONFIG_METRICS_BOT_ID] = self.bot_id
        config_manager.simple_save_config_update(self.edited_config)

    async def _post_community_data(self, route, bot, retry_on_error):
        try:
            async with self.session.post(f"{common_constants.METRICS_URL}{route}", json=bot,
                                         headers=self._headers) as resp:
                await self._handle_post_error(resp, retry_on_error)
        except Exception as e:
            self.logger.debug(f"Error when handling community data : {e}")

    async def _handle_post_error(self, resp, retry_on_error):
        if resp.status != 200:
            if resp.status == 404:
                # did not found bot with id in config: generate new id and register new bot
                if retry_on_error:
                    await self._init_bot_id()
                    await self.register_session(retry_on_error=False)
            else:
                self.logger.debug(f"Impossible to send community data : "
                                  f"status code: {resp.status}, "
                                  f"text: {await resp.text()}")
