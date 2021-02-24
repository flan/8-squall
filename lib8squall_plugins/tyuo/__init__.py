#since it's possible to message 8-squall directly, have it check the tpye of message.channel.
#if it's a direct-message/group-chat, always engage tyuo, without the need for the prefix string.

#add an explicit allow-list of people from whom learning can occur, on top of the channel-specific
#stuff; someone will need to issue the string "[t]yuo, you may learn from me[.]" or
#"tyuo, do not learn from me[.]"; make the help-text reflect this per-user (which means it can't be
# a static string, bur rather a function that takes the given message and client)

#never learn from messages that include mentions

#add a badwords filter on learning (and production) that disqualifies a string from being ingested.

#give each server its own personality instance
#should there be a per-user learning flag on a per-server basis? Probably.

#DMs have a shared instance of their own
#or maybe it shouldn't process anything in DMs, since keeping everything public is less-likely to
#allow it to learn toxic expressions

#Actually, each *channel* will have its own personality instance
#Multiple channels can be merged into a named group, through use of a map-file,
#but by default, each one will be standalone, to prevent bleed across topic domains
#and protect privacy

#opt-in/out will be universal on a per-user basis, since their fragments won't be
#able to propagate too far from where they were said, wherever that may have been
