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

import binascii
import sys

from cffi import FFI


# This is taken from https://caremad.io/2014/11/distributing-a-cffi-project/,
# which gives examples from cryptography
def _create_modulename(cdef_sources, source, sys_version):
    """
    This is the same as CFFI's create modulename except we don't include the
    CFFI version.
    """
    key = '\x00'.join([sys_version[:3], source, cdef_sources])
    key = key.encode('utf-8')
    k1 = hex(binascii.crc32(key[0::2]) & 0xffffffff)
    k1 = k1.lstrip('0x').rstrip('L')
    k2 = hex(binascii.crc32(key[1::2]) & 0xffffffff)
    k2 = k2.lstrip('0').rstrip('L')
    return '_pywayland_cffi_{0}{1}'.format(k1, k2)


CDEF = """
/******************************************************************************
 * wayland-version.h
 *****************************************************************************/
#define WAYLAND_VERSION_MAJOR ...
#define WAYLAND_VERSION_MINOR ...
#define WAYLAND_VERSION_MICRO ...

/******************************************************************************
 * wayland-util.h
 *****************************************************************************/
// Structs for event and request dispactching
typedef int32_t wl_fixed_t;
struct wl_message {
    const char *name;
    const char *signature;
    const struct wl_interface **types;
};
struct wl_interface {
    const char *name;
    int version;
    int method_count;
    const struct wl_message *methods;
    int event_count;
    const struct wl_message *events;
};
union wl_argument {
    int32_t i; /**< signed integer */
    uint32_t u; /**< unsigned integer */
    wl_fixed_t f; /**< fixed point */
    const char *s; /**< string */
    struct wl_object *o; /**< object */
    uint32_t n; /**< new_id */
    struct wl_array *a; /**< array */
    int32_t h; /**< file descriptor */
};

typedef int (*wl_dispatcher_func_t)(const void *, void *, uint32_t,
                                    const struct wl_message *,
                                    union wl_argument *);

// wl_fixed_t handling
static inline double wl_fixed_to_double(wl_fixed_t f);
static inline wl_fixed_t wl_fixed_from_double(double d);
static inline wl_fixed_t wl_fixed_from_int(int i);

/******************************************************************************
 * wayland-client.h
 *****************************************************************************/
// wl_display methods
struct wl_display* wl_display_connect(const char *name);
struct wl_display* wl_display_connect_to_fd(int fd);
struct wl_event_queue *wl_display_create_queue(struct wl_display *display);
void wl_display_disconnect(struct wl_display *display);
int wl_display_dispatch(struct wl_display *display);
int wl_display_dispatch_queue(struct wl_display *display,
                              struct wl_event_queue *queue);
int wl_display_dispatch_pending(struct wl_display *display);
int wl_display_flush(struct wl_display *display);
int wl_display_get_fd(struct wl_display *display);
int wl_display_roundtrip(struct wl_display *display);

// wl_eventqueue methods
void wl_event_queue_destroy(struct wl_event_queue *queue);

// wl_proxy methods
struct wl_proxy *wl_proxy_create(struct wl_proxy *factory,
                                 const struct wl_interface *interface);
void wl_proxy_destroy(struct wl_proxy *proxy);
int wl_proxy_add_dispatcher(struct wl_proxy *proxy,
                            wl_dispatcher_func_t dispatcher_func,
                            const void * dispatcher_data, void *data);
void *wl_proxy_get_user_data(struct wl_proxy *proxy);
void wl_proxy_marshal_array(struct wl_proxy *p, uint32_t opcode,
                            union wl_argument *args);
struct wl_proxy * wl_proxy_marshal_array_constructor(struct wl_proxy *proxy,
                                                     uint32_t opcode, union wl_argument *args,
                                                     const struct wl_interface *interface);
void wl_proxy_set_user_data(struct wl_proxy *proxy, void *user_data);
"""

SOURCE = """
#include <wayland-client.h>
#include <wayland-server.h>
#include <wayland-version.h>
"""

ffi = FFI()
ffi.cdef(CDEF)

C = ffi.verify(SOURCE,
               libraries=['wayland-client', 'wayland-server'],
               modulename=_create_modulename(CDEF, SOURCE, sys.version))
