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