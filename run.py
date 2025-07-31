from src.flask_app import app
import src.telegram_bot_api


def list_routes(app):
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        line = f"{rule.endpoint:30s} {methods:25s} {urllib.parse.unquote(str(rule))}"
        output.append(line)
    return output


if __name__ == '__main__':
    print("\n📦 Registered Flask Routes:")
    for route in list_routes(app):
        print("🔹", route)
    print(f"[run.py] app id: {id(app)}\n")

    # ✅ Bind to all interfaces (LAN-accessible)
    app.run(host='0.0.0.0', port=5000, debug=True)
