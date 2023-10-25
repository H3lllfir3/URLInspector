from discord_webhook import DiscordEmbed
from discord_webhook import DiscordWebhook


class DiscordNotification:

    def __init__(self, webhook_url: str) -> None:
        self.webhook = DiscordWebhook(url=webhook_url, username='URL Inspector')
        self.embed = DiscordEmbed
        self.STATUS = {
            'red': ':red_circle:',
            'green': ':green_circle:',
            'blue': ':blue_circle:',
        }

    def send_message(self, title: str, url: str, status: str) -> None:
        """Send a message to the webhook.

        Args:
            title (str): The title for the Discord message.
            url (str): The url for the Discord message.
        """
        embed = self.embed(title=f'{self.STATUS[status]}   {title}', description=f'{url}', color='03b2f8')
        embed.set_author(name='URL Inspector', url='https://github.com/H3lllfir3', icon_url='https://avatars.githubusercontent.com/u/55285134')
        embed.set_timestamp()

        self.webhook.add_embed(embed)
        self.webhook.execute()
