#!/usr/bin/ruby -Ku
#
# LINEWORKS::BOT シンプルフレームワーク SimpleFw (超適当版)
# Author: T.Mori
#
require 'uri'
require 'json'
require './lineworks'
require 'logger'

# -------
# コントローラ
# -------
module LineWorks
  class Controller
    # 初期化
    def initialize(body)
      @line = LineWorks::Bot.new("config.json", "private_rsa.key")
      @event, @account_id, @access_token = @line.callback(body)
      #next_screen(data["view"])
    end

    # タスク呼び出し
    def get_model(task)
      if task != nil and task != ""
        self.method(task)
      else
        self.method(:default)
      end
    end

    # 表示
    def exec(task = nil)
      case @event["type"]
      when LineWorks::Event::Message
        @m = get_model(:message).call(@event)
      when LineWorks::Event::Postback
        @data = @line.d(@event["data"])
        task = @data["task"] if task == nil
        @m = get_model(task).call(@data)
      end
    end

    # 遷移先
    def next_screen(view, alt, b)
      base_name = File.basename($0, ".*")
      screen = (view != nil and view != "") ? "#{view}" : base_name
      file_name = %(tmpl/#{view}.erb)

      content = @line.make_flex_contents(file_name, alt, b)
      @line.send_message(@access_token, @account_id, content)
    end

    # 簡易メッセージ送信
    def send_message(message)
      content = {"type": "text", "text": message}
      @line.send_message(@access_token, @account_id, content)
    end

    # テンプレート取得
    def get_views
      views = []
      Dir.glob("tmpl/*.erb") do |file|
        views << File.basename(file, ".*")
      end
      Struct.new("View", *views).new(*views)
    end
  end    
end

# eos #
