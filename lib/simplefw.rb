#!/usr/bin/ruby -Ku
#
# LINEWORKS::BOT シンプルフレームワーク SimpleFw (超適当版)
# Author: T.Mori
#
require 'uri'
require 'json'
require 'yaml'
require_relative 'lineworks'
require 'logger'

# -------
# コントローラ
# -------
module LineWorks
  class LibraryLoad
    def initialize
      # アプリ読み込み
      Dir.glob("app/*.rb").each do |file|
        if FileTest.file?(file)
          require "./#{file}"
        end
      end
    end
  end
  module Master
    def load_master(file)
      yaml = YAML.load_file(file)
      yaml.each do |key, val|
        instance_variable_set("@#{key}", val)
      end
    end
  end
  class Controller
    include Master
    # 初期化
    def initialize(body)
      if body.size > 10
        @line = LineWorks::Bot.new("config.json", "private_rsa.key")
        @event, @account_id, @access_token = @line.callback(body)
        @view = get_views
      end
    end

    # タスク呼び出し
    def get_model(task)
      task = nil if task !~ /^[\w\.]*$/
      if task != nil and task != ""
        params = task.split(".")
        app, meth = (params.size == 2) ? params : [self, params[0]]
        if (app != self)
          app = eval(app).new(@event, @account_id, @access_token, @view, self)
        end
        app.method(meth)
      else
        self.method(:default)
      end
    end

    # 表示
    def exec(task = nil)
      if @event != nil
        case @event["type"]
        when LineWorks::Event::Message
          @m = get_model("message").call(@event)
        when LineWorks::Event::Postback
          data = d(@event["data"])
          task = data["task"] if task == nil
          @m = get_model(task).call(data)
        end
      else
        get_model(nil).call(nil)
      end
    end

    # 遷移先
    def next_screen(view, alt, b)
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
    # レスポンス＆リクエストデータのencode/decode群
    def enc(data)
      URI.encode_www_form_component(data.to_json)
    end

    def dec(data)
      JSON.parse(URI.decode_www_form_component(data))
    end

    def d(data)
      Hash[URI.decode_www_form(data)]
    end

    def e(data)
      URI.encode_www_form(data)
    end

  end    
  class Application
    include Master
    def initialize(event, account_id, access_token, view, controller)
      @event = event
      @account_id = account_id
      @access_token = access_token
      @view = view
      @controller = controller
      init
    end

    def init
    end
  end
end

# eos #
