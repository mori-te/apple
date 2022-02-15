#
#
# Apple iPad 選択画面クラス
#
require './lib/simplefw'

class Ipad < LineWorks::Application
  # -------
  # Apple iPad
  # -------
  def init
    load_master('master.yaml')
  end

  # カラー選択画面（iPad）
  def flex_ipad(data)
    @controller.next_screen(@view.flex_ipad, "Apple iPad", binding)
  end

  # メモリサイズ選択（ipad）
  def flex_ipad_memory(data)
    color = data["color"]
    @controller.next_screen(@view.flex_ipad_memory, "Apple iPad", binding)
  end

  # モデル選択（ipad）
  def flex_ipad_model(data)
    color = data["color"]
    mem = data["mem"]
    @controller.next_screen(@view.flex_ipad_model, "Apple iPad", binding)
  end

  # 確認（ipad）
  def flex_ipad_confirm(data)
    data.delete("task")
    color = data["color"]
    mem = data["mem"]
    model = data["model"]
    type = data["type"]

    name, price1 = @PROD_TYPE[type]
    detail_options = [
      @COLOR_IPAD[color.to_i - 1],
      @MEMORY_IPAD[mem],
      @MODEL_IPAD[model.to_i - 1]
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
