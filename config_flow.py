from homeassistant import config_entries
from homeassistant.const import CONF_URL, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, CATEGORY_OPTIONS

class QBittorrentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=self._get_schema())

        url = user_input[CONF_URL]
        username = user_input[CONF_USERNAME]
        password = user_input[CONF_PASSWORD]

        # Here you would typically validate the connection to qBittorrent
        # For example, you could call a method to check if the credentials are correct

        return self.async_create_entry(title="qBittorrent", data=user_input)

    def _get_schema(self):
        from homeassistant.helpers import config_entry_flow
        from homeassistant.helpers import schema_builder

        return schema_builder.Schema(
            {
                CONF_URL: str,
                CONF_USERNAME: str,
                CONF_PASSWORD: str,
                "category": schema_builder.Select(CATEGORY_OPTIONS),
            }
        )