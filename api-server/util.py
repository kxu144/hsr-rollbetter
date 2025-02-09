import enka

client: enka.HSRClient = None

async def initialize_client():
    global client
    if client is None:
        cache = enka.cache.SQLiteCache()
        client = enka.HSRClient(enka.hsr.Language.ENGLISH, cache=cache)
        await client.update_assets()
    
    await client.start()

async def fetch_player_info(uid):
    await initialize_client()  # Ensure the client is initialized

    try:
        response = await client.fetch_showcase(uid)
    except enka.errors.PlayerDoesNotExistError:
        return {"error": "Player does not exist."}
    except enka.errors.GameMaintenanceError:
        return {"error": "Game is in maintenance."}

    player_data = {
        "name": response.player.nickname,
        "level": response.player.level,
        "equilibrium_level": response.player.equilibrium_level,
        "achievements": response.player.stats.achievement_count,
        "light_cones": response.player.stats.light_cone_count,
        "characters": response.player.stats.character_count,
        "profile_picture": response.player.icon,
        "characters_details": []
    }

    for character in response.characters:
        character_data = {
            "name": character.name,
            "level": f"{character.level}/{character.max_level}",
            "eidolons": character.eidolons_unlocked,
            "rarity": character.rarity,
            "element": character.element.name.title(),
            "path": character.path.name.title(),
            "light_cone": None,
            "stats": [],
            "dmg_bonus": None,
            "relics": []
        }

        lc = character.light_cone
        if lc:
            character_data["light_cone"] = {
                "name": lc.name,
                "level": f"{lc.level}/{lc.max_level}",
                "rarity": lc.rarity,
                "superimpose": lc.superimpose,
                "stats": [{"name": stat.name, "value": stat.formatted_value} for stat in lc.stats]
            }

        for stat in character.stats.values():
            if stat.value == 0 or stat.type.value in enka.hsr.DMG_BONUS_PROPS.values():
                continue
            character_data["stats"].append({"name": stat.name, "value": stat.formatted_value})

        if character.highest_dmg_bonus_stat:
            character_data["dmg_bonus"] = {
                "name": character.highest_dmg_bonus_stat.name,
                "value": character.highest_dmg_bonus_stat.formatted_value
            }

        for relic in character.relics:
            main_stat = relic.main_stat
            relic_data = {
                "type": relic.type.name,
                "set_name": relic.set_name,
                "level": relic.level,
                "main_stat": {
                    "name": main_stat.name,
                    "value": main_stat.formatted_value
                },
                "sub_stats": [
                    {"name": substat.name, "value": f"{substat.value}{'%' * substat.is_percentage}"} for substat in relic.sub_stats
                ]
            }
            character_data["relics"].append(relic_data)

        player_data["characters_details"].append(character_data)

    return player_data