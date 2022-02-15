#!/usr/bin/env /home/ts1/.rbenv/shims/ruby
# coding: utf-8
#
#!/bin/env ruby
#
# Lineworks Bot App.
#
require './lib/simplefw'

# -------
# メッセージ処理クラス
# -------
class AppController < LineWorks::Controller
  # 初期化
  def initialize(body)
    super(body)
    # マスタ取得
    load_master('master.yaml')
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
    type_name = @PROD_TYPE[type][0]
    date = Time.now.strftime("%Y/%m/%d %H:%M:%S")

    case type
    when "se"
      size = data["size"]
      color_name = @COLOR_SE[color.to_i - 1][0]
      size_name = @SIZE_SE[size][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{size_name},#{total_price}"
    when "7"
      size = data["size"]
      color_name = @COLOR_7[color.to_i - 1][0]
      size_name = @SIZE_7[size][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{size_name},#{total_price}"
    when "ipad"
      memory = data["mem"]
      model = data["model"]
      color_name = @COLOR_IPAD[color.to_i - 1][0]
      memory_name = @MEMORY_IPAD[memory][0]
      model_name = @MODEL_IPAD[model.to_i - 1][0]
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
  #body = '{"type":"postback","data":"task=Watchse.flex_se_size&type=se&color=2","source":{"accountId":"mori-te@tsone","roomId":"3231011"},"createdTime":1644295478892}'
  body = '{"type":"postback","data":"task=Watchse.flex_se_confirm&type=se&color=2&size=44","source":{"accountId":"mori-te@tsone","roomId":"129258418"},"createdTime":1643624240529}'
else
  body = $stdin.read
end

LineWorks::LibraryLoad.new
AppController.new(body).exec

# eos #
