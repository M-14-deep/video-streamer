from flask import Flask, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/api/v1/video/youtube/<video_id>', methods=["GET"])
def get_stream_url(video_id):
    # 対象となる動画 URL を作成
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # yt-dlp のオプション設定
    ydl_opts = {
        'quiet': True,           # ログ出力を抑制する
        'skip_download': True,   # 動画ファイルのダウンロードは行わない
        'format': 'best',        # 最高品質のストリームを選択
    }

    try:
        # yt-dlp を使って動画情報を抽出する
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            stream_url = info.get('url')
        
        if stream_url:
            return jsonify({'streamurl': stream_url})
        else:
            # ストリーム URL が無い場合の例外処理
            return jsonify({'error': 'ストリーム URL が取得できませんでした'}), 404
    except Exception as e:
        # エラー発生時はエラーメッセージを返す
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # デバッグモードで実行（実運用時は適宜変更してください）
    app.run(host='0.0.0.0', port=5000, debug=True)
