# cython: language_level=3
#  gd2003gamingchamp OctoIFX
#  Copyright (c) gd2003gamingchamp, All rights reserved.
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
cimport octobot.channels as octobot_channels


cdef class ServiceFeedProducer(octobot_channels.OctoBotChannelProducer):
    cdef public object octobot
    cdef public bint started

    cdef public list service_feeds
