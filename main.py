import vk
import user
import json

f = open('token.json', 'r')
tokens = json.loads(f.read())
f.close()

c = vk.Client(tokens['bot_token'], tokens['audio_token'], tokens['group_id'])

users = {}

while True:
    um = c.get_unread_messages()
    if um is None:
        continue

    for m in um:
        uid = m['uid']

        # unregistered user
        if users.get(uid, 0) == 0:
            ok = c.send_message(uid, vk.HELLO_MESSAGE)
            if ok:
                users.update({uid: user.User(uid, user.STATE_NEW)})

            continue

        # /create
        if users[uid].state == user.STATE_NEW:

            if m['body'].find('/create') != -1:
                ok = c.send_message(uid, vk.PLAYLIST_NAMING)
                if ok:
                    users[uid].change_state(user.STATE_PLAYLIST_NAMING)
            else:
                c.send_message(uid, 'Hey, bro, write /create of GTFO')

        # playlist naming
        elif users[uid].state == user.STATE_PLAYLIST_NAMING:
            name = m['body']
            pid = c.create_playlist(name)

            if pid is not None:
                users[uid].pid = pid
                users[uid].change_state(user.STATE_PLAYLIST_ADD)
                msg = 'Your playlist name is a <%s>. Send me tracks!' % name
            else:
                msg = 'Internal error! (creating album)'

            c.send_message(uid, msg)

        # adding songs
        elif users[uid].state == user.STATE_PLAYLIST_ADD:
            if m.get('attachments', False):
                users[uid].add_tracks([el for el in m['attachments'] if el['type'] == 'audio'])
                msg = 'You added %d tracks total. Write "/finish", when you finish (lol)' \
                      % users[uid].get_tracks_count()

                c.send_message(uid, msg)

            # finish
            if m['body'].find('/finish') != -1:
                failed = False
                for t in reversed(users[uid].get_tracks()):
                    if not c.add_track(users[uid].pid, t['audio']['aid'], t['audio']['owner_id']):
                        failed = True
                        break

                if not failed:
                    msg = 'Thank you. Your playlist is here! https://vk.com/audios-%d?album_id=%d .' % \
                          (tokens['group_id'], users[uid].pid)
                else:
                    msg = 'Internal error! ' \
                          'Sorry. Anyway, you have %d tracks. Check https://vk.com/audios-%d?album_id=%d .' \
                          % (users[uid].get_tracks_count(), tokens['group_id'], users[uid].pid)

                c.send_message(uid, msg)
                try:
                    users.pop(uid)
                except KeyError:
                    print('Oh fuck! users["%d"] isn`t exist!' % uid)
