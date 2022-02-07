#
#
# Apple Watch SE 選択画面クラス
#
require 'yaml'
require './lib/simplefw'

class Watchse < LineWorks::Application
  # -------
  # Apple Watch se
  # -------
  def init
    @master = YAML.load_file('master.yaml')
  end

  # カラー選択画面（SE）
  def flex_watchse(data)
    @controller.next_screen(@view.flex_watchse, "Apple Watch se", binding)
  end

  # サイズ選択（SE）
  def flex_se_size(data)
    color = data["color"]
    @controller.next_screen(@view.flex_se_size, "Apple Watch se", binding)
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
    data_string = @controller.e(data)
    @controller.next_screen(@view.confirm, name, binding)
  end

end
