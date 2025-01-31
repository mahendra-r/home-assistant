"""
homeassistant.components.alarm_control_panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Component to interface with a alarm control panel.
"""
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components import verisure
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_ALARM_DISARM, SERVICE_ALARM_ARM_HOME, SERVICE_ALARM_ARM_AWAY)

DOMAIN = 'alarm_control_panel'
DEPENDENCIES = []
SCAN_INTERVAL = 30

ENTITY_ID_FORMAT = DOMAIN + '.{}'

# Maps discovered services to their platforms
DISCOVERY_PLATFORMS = {
    verisure.DISCOVER_SENSORS: 'verisure'
}

SERVICE_TO_METHOD = {
    SERVICE_ALARM_DISARM: 'alarm_disarm',
    SERVICE_ALARM_ARM_HOME: 'alarm_arm_home',
    SERVICE_ALARM_ARM_AWAY: 'alarm_arm_away',
}

ATTR_CODE = 'code'
ATTR_CODE_FORMAT = 'code_format'

ATTR_TO_PROPERTY = [
    ATTR_CODE,
    ATTR_CODE_FORMAT
]


def setup(hass, config):
    """ Track states and offer events for sensors. """
    component = EntityComponent(
        logging.getLogger(__name__), DOMAIN, hass, SCAN_INTERVAL,
        DISCOVERY_PLATFORMS)

    component.setup(config)

    def alarm_service_handler(service):
        """ Maps services to methods on Alarm. """
        target_alarms = component.extract_from_service(service)

        if ATTR_CODE not in service.data:
            return

        code = service.data[ATTR_CODE]

        method = SERVICE_TO_METHOD[service.service]

        for alarm in target_alarms:
            getattr(alarm, method)(code)

    for service in SERVICE_TO_METHOD:
        hass.services.register(DOMAIN, service, alarm_service_handler)

    return True


def alarm_disarm(hass, code, entity_id=None):
    """ Send the alarm the command for disarm. """
    data = {ATTR_CODE: code}

    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id

    hass.services.call(DOMAIN, SERVICE_ALARM_DISARM, data)


def alarm_arm_home(hass, code, entity_id=None):
    """ Send the alarm the command for arm home. """
    data = {ATTR_CODE: code}

    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id

    hass.services.call(DOMAIN, SERVICE_ALARM_ARM_HOME, data)


def alarm_arm_away(hass, code, entity_id=None):
    """ Send the alarm the command for arm away. """
    data = {ATTR_CODE: code}

    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id

    hass.services.call(DOMAIN, SERVICE_ALARM_ARM_AWAY, data)


# pylint: disable=no-self-use
class AlarmControlPanel(Entity):
    """ ABC for alarm control devices. """

    @property
    def code_format(self):
        """ regex for code format or None if no code is required """
        return None

    def alarm_disarm(self, code=None):
        """ Send disarm command. """
        raise NotImplementedError()

    def alarm_arm_home(self, code=None):
        """ Send arm home command. """
        raise NotImplementedError()

    def alarm_arm_away(self, code=None):
        """ Send arm away command. """
        raise NotImplementedError()

    @property
    def state_attributes(self):
        """ Return the state attributes. """
        state_attr = {
            ATTR_CODE_FORMAT: self.code_format,
            }
        return state_attr
