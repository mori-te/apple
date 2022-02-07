#!/usr/bin/env /home/ts1/.rbenv/shims/ruby
# coding: utf-8
#
#!/bin/env ruby
#
# Lineworks Bot App.
#
require 'yaml'
require 'pp'
require './lib/simplefw'

# -------
# メッセージ処理クラス
# -------
class AppController < LineWorks::Controller
  # 初期化
  def initialize(body)
    super(body)
    # マスタ取得
    @master = YAML.load_file('master.yaml')
  end

  # デフォルト表示
  def default(body)
    print "Content-Type: text/plain\n\n"
  end

  # メッセージ受信
  def message(event)
    # 商品選択画面
    next_screen(@view.flex_menu, "Apple Watch/iPad", binding)
  end

  # -------
  # 共通処理
  # -------

  # 確定処理
  def send(data)
    buffer = nil
    type = data["type"]
    color = data["color"]
    total_price = data["total_price"]
    type_name = @master["PROD_TYPE"][type][0]
    date = Time.now.strftime("%Y/%m/%d %H:%M:%S")

    case type
    when "se"
      size = data["size"]
      color_name = @master["COLOR_SE"][color.to_i - 1][0]
      size_name = @master["SIZE_SE"][size][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{size_name},#{total_price}"
    when "7"
      size = data["size"]
      color_name = @master["COLOR_7"][color.to_i - 1][0]
      size_name = @master["SIZE_7"][size][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{size_name},#{total_price}"
    when "ipad"
      memory = data["mem"]
      model = data["model"]
      color_name = @master["COLOR_IPAD"][color.to_i - 1][0]
      memory_name = @master["MEMORY_IPAD"][memory][0]
      model_name = @master["MODEL_IPAD"][model.to_i - 1][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{memory_name},#{model_name},#{total_price}"
    end

    File.open("regist.csv", "a") do |io|
      io.flock(File::LOCK_EX)
      io.puts(buffer)
      io.flock(File::LOCK_UN)
    end
    send_message("受け付けました。")
  end

  # やり直し
  def retry(data)
    send_message("もう一度最初から選択してください。")
    next_screen(@view.flex_menu, "Apple Watch/iPad", binding)
  end

end

# -------
# for MAIN
# -------
include Logger::Severity
$log = Logger.new('callback.log')

if ARGV.size > 0
  #body = '{"type":"message","source":{"accountId":"tetsu@mo-net"},"createdTime":1643360355161,"content":{"type":"text","text":"TEST"}}'
  #body = '{"type":"postback","data":"task=Watchse.flex_watchse&type=Watchse","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=Ipad.flex_ipad&type=ipad","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=Watchse.flex_se_size&type=se&color=2","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=Watchse.flex_se_confirm&type=se&color=2&size=44","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=Watch7.flex_7_confirm&type=se&color=2&size=45","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  body = '{"type":"postback","data":"task=Ipad.flex_ipad_confirm&type=ipad\u0026color=2&mem=256&model=2","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback", "data":"task=send&type=ipad&color=2&mem=256&model=2&total_price=43000", "source":{"accountId":"tetsu@mo-net", "roomId":"129258418"}, "createdTime":1643865231519}'
  #body = '{"type":"postback", "data":"task=retry", "source":{"accountId":"tetsu@mo-net", "roomId":"129258418"}, "createdTime":1643865332470}'
  #body = ''
else
  body = $stdin.read
end

LineWorks::LibraryLoad.new
AppController.new(body).exec

# eos #
