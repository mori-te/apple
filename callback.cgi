#!/usr/bin/env /home/binder/.rbenv/shims/ruby
# coding: utf-8
#
#!/bin/env ruby
#
# Lineworks Bot App.
#
require 'yaml'
require 'pp'
require './simplefw'

# -------
# メッセージ処理クラス
# -------
class AppController < LineWorks::Controller
  # 初期化
  def initialize(body)
    super(body)
    # マスタ取得
    @master = YAML.load_file('master.yaml')
    @view = get_views
  end

  # メッセージ受信
  def message(event)
    # 商品選択画面
    next_screen(@view.flex_menu, "Apple Watch/iPad", binding)
  end

  # -------
  # Apple Watch SE
  # -------

  # カラー選択画面（SE）
  def flex_watchse(data)
    next_screen(@view.flex_watchse, "Apple Watch se", binding)
  end

  # サイズ選択（SE）
  def flex_se_size(data)
    color = data["color"]
    next_screen(@view.flex_se_size, "Apple Watch se", binding)
  end

  # 確認（SE）
  def flex_se_confirm(data)
    data.delete("task")
    color = data["color"]
    size = data["size"]
    type = data["type"]

    name, price1 = @master["PROD_TYPE"][type]
    detail_options = [
        @master["COLOR_SE"][color.to_i - 1],
        @master["SIZE_SE"][size]
    ]
    detail_price_total = 0
    detail_options.each do |name, price|
        detail_price_total += price
    end
    total_price = (detail_price_total + price1)
    today = Time.now.strftime("%Y/%m/%d %H:%M:%S")

    data["total_price"] = total_price
    data_string = @line.e(data)
    next_screen(@view.confirm, name, binding)
  end

  # -------
  # Apple Watch 7
  # -------

  # カラー選択画面（7）
  def flex_watch7(data)
    next_screen(@view.flex_watch7, "Apple Watch 7", binding)
  end

  # サイズ選択（7）
  def flex_7_size(data)
    color = data["color"]
    next_screen(@view.flex_7_size, "Apple Watch 7", binding)
  end

  # 確認（7）
  def flex_7_confirm(data)
    data.delete("task")
    color = data["color"]
    size = data["size"]
    type = data["type"]

    name, price1 = @master["PROD_TYPE"][type]
    detail_options = [
        @master["COLOR_7"][color.to_i - 1],
        @master["SIZE_7"][size]
    ]
    detail_price_total = 0
    detail_options.each do |name, price|
        detail_price_total += price
    end
    total_price = (detail_price_total + price1)
    today = Time.now.strftime("%Y/%m/%d %H:%M:%S")

    data["total_price"] = total_price
    data_string = @line.e(data)
    next_screen(@view.confirm, name, binding)
  end

  # -------
  # Apple iPad
  # -------

  # カラー選択画面（iPad）
  def flex_ipad(data)
    next_screen(@view.flex_ipad, "Apple iPad", binding)
  end

  # メモリサイズ選択（ipad）
  def flex_ipad_memory(data)
    color = data["color"]
    next_screen(@view.flex_ipad_memory, "Apple iPad", binding)
  end

  # モデル選択（ipad）
  def flex_ipad_model(data)
    color = data["color"]
    mem = data["mem"]
    next_screen(@view.flex_ipad_model, "Apple iPad", binding)
  end

  # 確認（ipad）
  def flex_ipad_confirm(data)
    data.delete("task")
    color = data["color"]
    mem = data["mem"]
    model = data["model"]
    type = data["type"]

    name, price1 = @master["PROD_TYPE"][type]
    detail_options = [
        @master["COLOR_IPAD"][color.to_i - 1],
        @master["MEMORY_IPAD"][mem],
        @master["MODEL_IPAD"][model.to_i - 1]
    ]
    detail_price_total = 0
    detail_options.each do |name, price|
        detail_price_total += price
    end
    total_price = (detail_price_total + price1)
    today = Time.now.strftime("%Y/%m/%d %H:%M:%S")

    data["total_price"] = total_price
    data_string = @line.e(data)
    next_screen(@view.confirm, name, binding)
  end  

  # -------
  # その他処理
  # -------

  # 確定処理
  def send(data)
    buffer = nil
    type = data["type"]
    color = data["color"]
    total_price = data["total_price"]
    date = Time.now.strftime("%Y/%m/%d %H:%M:%S")

    case type
    when "se"
      size = data["size"]
      type_name = @master["PROD_TYPE"][type][0]
      color_name = @master["COLOR_SE"][color.to_i - 1][0]
      size_name = @master["SIZE_SE"][size][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{size_name},#{total_price}"
    when "7"
      size = data["size"]
      type_name = @master["PROD_TYPE"][type][0]
      color_name = @master["COLOR_7"][color.to_i - 1][0]
      size_name = @master["SIZE_7"][size][0]
      buffer = "#{@account_id},#{date},#{type_name},#{color_name},#{size_name},#{total_price}"
    when "ipad"
      memory = data["mem"]
      model = data["model"]
      type_name = @master["PROD_TYPE"][type][0]
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
  body = '{"type":"message","source":{"accountId":"tetsu@mo-net"},"createdTime":1643360355161,"content":{"type":"text","text":"TEST"}}'
  #body = '{"type":"postback","data":"task=flex_watchse&type=se","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=flex_se_size&type=se&color=2","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=flex_se_confirm&type=se&color=2&size=44","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=flex_7_confirm&type=se&color=2&size=45","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback","data":"task=flex_ipad_confirm&type=ipad\u0026color=2&mem=256&model=2","source":{"accountId":"tetsu@mo-net","roomId":"129258418"},"createdTime":1643624240529}'
  #body = '{"type":"postback", "data":"task=send&type=ipad&color=2&mem=256&model=2&total_price=43000", "source":{"accountId":"tetsu@mo-net", "roomId":"129258418"}, "createdTime":1643865231519}'
  #body = '{"type":"postback", "data":"task=retry", "source":{"accountId":"tetsu@mo-net", "roomId":"129258418"}, "createdTime":1643865332470}'
else
  body = $stdin.read
end

AppController.new(body).exec

# eos #
