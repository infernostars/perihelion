import json
import os
from typing import Optional, List, Any
from discord import app_commands, Locale
from discord.app_commands import TranslationContext, TranslationContextLocation, locale_str

class JSONTranslator(app_commands.Translator):
    def __init__(self):
        self.translations = {}

    async def load(self):
        assets_dir = 'assets/translation'
        for filename in os.listdir(assets_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Remove .json extension
                with open(os.path.join(assets_dir, filename), 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)

    async def translate(self, string: locale_str, locale: Locale, context: TranslationContext) -> Optional[str]:
        lang_code = str(locale)

        if lang_code not in self.translations:
            lang_code = "en-US"

        if context.location == TranslationContextLocation.parameter_description or context.location == TranslationContextLocation.command_description:
            locale_str(f"{string}.desc")

        translation = self.translations[lang_code].get(str(string))

        if translation is None:
            return None

        if context.data and context.location == TranslationContextLocation.other:
            for i, replacement in enumerate(context.data, start=1):
                translation = translation.replace(f'%{i}', str(replacement))

        return translation

# this isnt complete so
