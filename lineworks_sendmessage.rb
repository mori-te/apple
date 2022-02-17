#
#
#
require './lib/lineworks'

@line = LineWorks::Bot.new("config.json", "private_rsa.key")

account_ids = []
File.open("account.dat", "r").each(chomp: true) do |buf|
  if buf !~ /^ *#/
    account_ids << buf
  end
end

#account_ids = ["mori-te@tsone"]


account_ids.each do |account_id|
  ret = @line.get_server_token(@line.get_jwt)
  access_token = ret["access_token"]
    #content = {"type": "text", "text": "テストです。"}
  content = @line.make_flex_contents("tmpl/flex_menu.erb", "Apple Watch/iPad", binding)
  res = @line.send_message(access_token, account_id, content)
  p "#{account_id}: #{res}"
  sleep 1
end
