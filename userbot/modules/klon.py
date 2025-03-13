#credit by @silgiuserbot

from telethon.tl.functions.photos import GetUserPhotosRequest, UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl import functions
from userbot.events import register
from userbot import BRAIN_CHECKER, WHITELIST
from userbot.language import get_value

LANG = get_value("userbot")

old_first_name = None
old_last_name = None
old_profile_photo = None
old_bio = None

@register(outgoing=True, pattern="^.klon ?(.*)")
async def clone(event):
    global old_first_name, old_last_name, old_profile_photo, old_bio
    if event.fwd_from:
        return

    replied_user = await get_user(event)
    
    if replied_user is None:
        await event.edit("❗ User tapılmadı. User seçdiyindən əminsən?")
        return
    
    if replied_user.id in BRAIN_CHECKER or replied_user.id in WHITELIST:
        await event.edit(LANG['SILGI'])
        return

    me = await event.client.get_me()
    old_first_name = me.first_name
    old_last_name = me.last_name
    old_profile_photo = await event.client.download_profile_photo("me")
    full_user = await event.client(functions.users.GetFullUserRequest(me.id))
    old_bio = full_user.bio if hasattr(full_user, "bio") else None

    first_name = replied_user.first_name or ""
    last_name = replied_user.last_name or ""
    
    replied_full_user = await event.client(functions.users.GetFullUserRequest(replied_user.id))
    bio = replied_full_user.bio if hasattr(replied_full_user, "bio") else None

    await event.client(functions.account.UpdateProfileRequest(
        first_name=first_name,
        last_name=last_name
    ))

    if bio:
        await event.client(functions.account.UpdateProfileRequest(about=bio))

    profile_pic = await event.client.download_profile_photo(replied_user.id)
    if profile_pic:
        uploaded_photo = await event.client.upload_file(profile_pic)
        await event.client(functions.photos.UploadProfilePhotoRequest(file=uploaded_photo))
        await event.edit("✅ Axalay maxalay puf! Profil klonlandı.")
    else:
        await event.respond("⚠️ Profil şəkli tapılmadı. Sadəcə ad və bio klonlandı.", reply_to=event)

@register(outgoing=True, pattern="^.revert$")
async def revert(event):
    global old_first_name, old_last_name, old_profile_photo, old_bio
    if event.fwd_from:
        return

    if not (old_first_name or old_last_name or old_profile_photo or old_bio):
        await event.edit("❗ Köhnə profil məlumatları tapılmadı.")
        return

    await event.client(functions.account.UpdateProfileRequest(
        first_name=old_first_name,
        last_name=old_last_name
    ))

    if old_bio:
        await event.client(functions.account.UpdateProfileRequest(about=old_bio))

    if old_profile_photo:
        uploaded_photo = await event.client.upload_file(old_profile_photo)
        await event.client(functions.photos.UploadProfilePhotoRequest(file=uploaded_photo))

    await event.edit("✅ Axalay maxalay puf! Profil geri qayıtdı.")

async def get_user(event):
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        return await event.client.get_entity(reply_message.sender_id)
    elif event.pattern_match.group(1):
        user = event.pattern_match.group(1)
        if user.isnumeric():
            return await event.client.get_entity(int(user))
        else:
            try:
                return await event.client.get_entity(user)
            except ValueError:
                return None
    return None
