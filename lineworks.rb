#
# LineWorks Bot Library (超適当版)
# Author: T.Mori
#
require 'uri'
require 'net/http'
require 'erb'
require 'json'
require 'jwt'     # gem install jwt
require 'logger'
require 'pp'

module LineWorks
  module Event
    Message = "message"
    Postback = "postback"
  end
  class Bot

    # 初期化
    def initialize(config_file, private_key)
      config_data = JSON.parse(File.open(config_file).read)
      @api_id = config_data["APIID"]
      @server_id = config_data["SERVERID"]
      @consumer_key = config_data["CONSUMERKEY"]
      @private_key = File.open(private_key).read
      @bot_no = config_data["BOTNO"]
    end

    # HTTP
    def get_http(token_url)
      uri = URI.parse(token_url)
      req = Net::HTTP::Post.new(uri)
      yield req
      req_options = {:use_ssl => uri.scheme == "https"}
      Net::HTTP.start(uri.host, uri.port, req_options) {|http| http.request(req)}
    end

    # JWT作成・電子署名
    def get_jwt
      iss = @server_id
      iat = Time.now.to_i
      exp = iat + 3600
      cert =OpenSSL::PKey::RSA.new(@private_key)
      JWT.encode({iss:iss, iat:iat, exp:exp}, cert, 'RS256')
    end

    # サーバトークン取得
    def get_server_token(token)
      # https://developers.worksmobile.com/jp/document/1002002?lang=ja
      token_url = "https://authapi.worksmobile.com/b/#{@api_id}/server/token"
      res = get_http(token_url) do |req|
        req["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
        req.set_form_data({grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: token})
      end
      JSON.parse(res.body)
    end

    # メッセージ送信
    def send_message(token, account_id, content)
      # https://developers.worksmobile.com/jp/document/1005008?lang=ja
      send_url = "https://apis.worksmobile.com/r/#{@api_id}/message/v1/bot/#{@bot_no}/message/push"
      res = get_http(send_url) do |req|
        req["Content-Type"] = "application/json;charset=UTF-8"
        req["consumerKey"] = @consumer_key
        req["Authorization"] = "Bearer #{token}"
        req.body ={botNo: @bot_no, accountId: account_id, content: content}.to_json
        pp req.body
      end
      p res.body
    end

    # コンテンツ作成
    def make_contents(template, b)
      JSON.parse(ERB.new(File.open(template).read).result(b))
    end

    # コンテンツ作成（Flex）
    def make_flex_contents(template, alt, b)
      temp = ERB.new("<%# encoding: UTF-8 %>\n" + File.open(template).read).result(b)
      ret = {
        "type": "flex",
        "altText": alt,
        "contents": JSON.parse(temp)
      }
      ret
    end

    # コールバック処理
    def callback(body)
      event = JSON.parse(body)
      account_id = event["source"]["accountId"]
      token_res = get_server_token(get_jwt)
      access_token = token_res["access_token"]
      $log.add(INFO, event)
      yield event, account_id, access_token if block_given?
      [event, account_id, access_token]
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
end