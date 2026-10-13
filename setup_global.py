import os
import subprocess
import sys

print("🚀 [Termux Master] A verificar o ambiente global...")

# Verificar dependências essenciais no Termux
try:
    import kivy
    print("✅ [OK] Kivy detetado no ambiente global.")
except ImportError:
    print("⚠️ [Aviso]: Kivy não encontrado. A instalar globalmente...")
    subprocess.run([sys.executable, "-m", "pip", "install", "kivy"], check=True)

# Criar pastas do projeto
os.makedirs(".github/workflows", exist_ok=True)

# Criar o main.py
main_code = """from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MeuApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="App Global no Termux 🚀", font_size=20)
        botao = Button(text='Testar', font_size=24, background_color=(0.1, 0.5, 0.8, 1))
        botao.bind(on_press=self.mudar_texto)
        layout.add_widget(self.label)
        layout.add_widget(botao)
        return layout

    def mudar_texto(self, instance):
        self.label.text = "Tudo a funcionar perfeitamente! 🔥"

if __name__ == '__main__':
    MeuApp().run()
"""
with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)

# Criar buildozer.spec
spec_code = """[app]
title = AppGlobal
package.name = appglobal
package.domain = org.termux
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
"""
with open("buildozer.spec", "w", encoding="utf-8") as f:
    f.write(spec_code)

# Criar GitHub Actions workflow
workflow_code = """name: Compilar APK Android

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Descarregar Código
        uses: actions/checkout@v4

      - name: Compilar com Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          command: buildozer -v android debug
          buildozer_version: stable

      - name: Guardar o APK Gerado (Artifact)
        uses: actions/upload-artifact@v4
        with:
          name: app-global-debug
          path: ${{ steps.buildozer.outputs.filename }}
"""
with open(".github/workflows/build.yml", "w", encoding="utf-8") as f:
    f.write(workflow_code)

print("✅ Estrutura do projeto gerada com sucesso!")

# Automação do Git
if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)

subprocess.run(["git", "config", "user.name", "TermuxMaster"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["git", "config", "user.email", "master@termux.dev"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Setup global automático"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["git", "branch", "-M", "main"], check=True)

print("\n--------------------------------------------------")
repo_url = input("🔗 Cole o URL do repositório GitHub: ").strip()
token = input("🔑 Cole o seu Token do GitHub: ").strip()
print("--------------------------------------------------")

if repo_url and token:
    if "https://" in repo_url:
        auth_url = repo_url.replace("https://", f"https://{token}@")
    else:
        auth_url = f"https://{token}@{repo_url}"

    subprocess.run(["git", "remote", "remove", "origin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", auth_url], check=True)

    print("🚀 A enviar para o GitHub...")
    res = subprocess.run(["git", "push", "-f", "-u", "origin", "main"])

    if res.returncode == 0:
        print("\n🎉 SUCESSO TOTAL! O Termux preparou tudo e enviou para a nuvem!")
    else:
        print("\n❌ Erro no envio. Verifique o seu Token e URL.")
else:
    print("\n⚠️ URL ou Token em falta.")

