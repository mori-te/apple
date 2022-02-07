#
#
# Apple Watch 7 選択画面クラス
#
require 'yaml'
require './lib/simplefw'

class Watch7 < LineWorks::Application
  # -------
  # Apple Watch 7
  # -------
  def init
    @master = YAML.load_file('master.yaml')
  end

  # カラー選択画面（7）
  def flex_watch7(data)
    @controller.next_screen(@view.flex_watch7, "Apple Watch 7", binding)
  end

  # サイズ選択（7）
  def flex_7_size(data)
    color = data["color"]
    @controller.next_screen(@view.flex_7_size, "Apple Watch 7", binding)
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
    data_string = @controller.e(data)
    @controller.next_screen(@view.confirm, name, binding)
  end

end
