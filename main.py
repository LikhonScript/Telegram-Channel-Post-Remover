import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from rich.console import Console
from rich.panel import Panel
import logging
from rich.text import Text
from rich.logging import RichHandler
from rich.progress import track

# Setup rich console and logging
console = Console()
logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(console=console)])

api_id = '25926417'  # Substitua com seu api_id
api_hash = '812a2f35614cccc19b432beeed96ef1e'  # Substitua com seu api_hash
channel_id = -1002046964190  # Substitua com o ID do seu canal

client = TelegramClient('session_name', api_id, api_hash)

def print_credits():
    credit_text = Text("Made by @LikhonScripts", style="bold magenta")
    panel = Panel(credit_text, expand=False)
    console.print(panel, justify="center")

async def delete_all_messages(channel_id):
    channel_entity = PeerChannel(channel_id)
    message_ids = []
    async for message in client.iter_messages(channel_entity):
        message_ids.append(message.id)
        if len(message_ids) >= 100:
            try:
                await client.delete_messages(channel_entity, message_ids)
                console.log(f"[bold green]Deleted {len(message_ids)} messages.[/bold green]")
                message_ids = []
                await asyncio.sleep(2)
            except Exception as e:
                console.log(f"[bold red]Error in bulk deletion: {e}[/bold red]")

    if message_ids:
        try:
            await client.delete_messages(channel_entity, message_ids)
            console.log(f"[bold green]Deleted {len(message_ids)} messages.[/bold green]")
        except Exception as e:
            console.log(f"[bold red]Error in final bulk deletion: {e}[/bold red]")

async def main():
    await client.start()
    print_credits()
    console.log("[bold cyan]Client started. Fetching channel messages...[/bold cyan]")
    try:
        for _ in track(range(100), description="Processing..."):
            await asyncio.sleep(0.1)  # Simulated task
        await delete_all_messages(channel_id)
    finally:
        await client.disconnect()
        console.log("[bold magenta]Client disconnected.[/bold magenta]")

if __name__ == "__main__":
    asyncio.run(main())