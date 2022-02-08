# This file has been autogenerated by the pywayland scanner

# Copyright 2015 Sean Vig
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import enum

from pywayland.protocol_core import (
    Argument,
    ArgumentType,
    Global,
    Interface,
    Proxy,
    Resource,
)
from .wl_requests import WlRequests


class WlCore(Interface):
    """Interface object

    The interface object with the most basic content.
    """

    name = "wl_core"
    version = 1

    class the_enum(enum.IntEnum):
        zero = 0
        one = 1
        hex_two = 0x2


class WlCoreProxy(Proxy[WlCore]):
    interface = WlCore

    @WlCore.request(
        Argument(ArgumentType.NewId, interface=WlCore),
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Fixed),
    )
    def make_request(
        self, the_int: int, the_uint: int, the_fixed: float
    ) -> Proxy[WlCore]:
        """A request

        The request asks the server for an event.

        :param the_int:
            the arg summary
        :type the_int:
            `ArgumentType.Int`
        :param the_uint:
        :type the_uint:
            `ArgumentType.Uint`
        :param the_fixed:
        :type the_fixed:
            `ArgumentType.Fixed`
        :returns:
            :class:`WlCore`
        """
        id = self._marshal_constructor(0, WlCore, the_int, the_uint, the_fixed)
        return id

    @WlCore.request(
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Fixed),
        Argument(ArgumentType.NewId, interface=WlCore),
    )
    def make_request2(
        self, the_int: int, the_uint: int, the_fixed: float
    ) -> Proxy[WlCore]:
        """A request

        The request asks the server for an event but move the args around.

        :param the_int:
            the arg summary
        :type the_int:
            `ArgumentType.Int`
        :param the_uint:
        :type the_uint:
            `ArgumentType.Uint`
        :param the_fixed:
        :type the_fixed:
            `ArgumentType.Fixed`
        :returns:
            :class:`WlCore` -- a :class:`WlCore` object
        """
        id = self._marshal_constructor(1, WlCore, the_int, the_uint, the_fixed)
        return id


class WlCoreResource(Resource):
    interface = WlCore

    @WlCore.event(
        Argument(ArgumentType.NewId, interface=WlCore),
        Argument(ArgumentType.Object, interface=WlRequests),
    )
    def send_event(self, id: WlCore, object: WlRequests) -> None:
        """A :class:`WlCore` event

        Send an event, but also put in some docs for our interface
        :class:`WlCore`, some other interface wl_other, a local function call
        :func:`WlCore.func()`, and another function call wl_other.func.

        :param id:
            a :class:`WlCore` object
        :type id:
            :class:`WlCore`
        :param object:
            a :class:`~pywayland.protocol.scanner_test.WlRequests` object
        :type object:
            :class:`~pywayland.protocol.scanner_test.WlRequests`
        """
        self._post_event(0, id, object)


class WlCoreGlobal(Global):
    interface = WlCore


WlCore._gen_c()
WlCore.proxy_class = WlCoreProxy
WlCore.resource_class = WlCoreResource
WlCore.global_class = WlCoreGlobal
