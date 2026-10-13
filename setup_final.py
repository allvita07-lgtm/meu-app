import os
import subprocess
import sys

print("🚀 [Automação Direta] A criar a estrutura do projeto...")

# 1. Garantir pastas corretas
os.makedirs(".github/workflows", exist_ok=True)
print("📁 [OK] Pastas do GitHub Actions criadas.")

# 2. Criar o ficheiro principal da app (main.py)
main_code = """from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MeuApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="App Criada no Termux 🚀", font_size=20)
        botao = Button(text='Clique Aqui', font_size=24, background_color=(0.1, 0.5, 0.8, 1))
        botao.bind(on_press=self.mudar_texto)

        layout.add_widget(self.label)
        layout.add_widget(botao)
        return layout

    def mudar_texto(self, instance):
        self.label.text = "Compilado com Sucesso na Nuvem! 🔥"

if __name__ == '__main__':
    MeuApp().run()
"""
with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)
print("✅ [OK] Ficheiro 'main.py' criado.")

# 3. Criar o buildozer.spec
spec_code = """[app]
title = MeuAppNuvem
package.name = meuappnuvem
package.domain = org.termux
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET
"""
with open("buildozer.spec", "w", encoding="utf-8") as f:
    f.write(spec_code)
print("✅ [OK] Ficheiro 'buildozer.spec' criado.")

# 4. Criar o fluxo do GitHub Actions
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
          name: meu-app-debug
          path: ${{ steps.buildozer.outputs.filename }}
"""
with open(".github/workflows/build.yml", "w", encoding="utf-8") as f:
    f.write(workflow_code)
print("✅ [OK] Ficheiro do GitHub Actions criado.")

# 5. Configuração do Git e Envio Automático com Token
print("\n🔍 A preparar o envio via Git...")
try:
    git_check = subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if git_check.returncode != 0:
        print("❌ Erro: O Git não está instalado. Instale com: pkg install git -y")
        sys.exit(1)

    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    subprocess.run(["git", "config", "user.name", "TermuxBot"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.email", "bot@termux.dev"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Setup projeto Kivy para GitHub Actions"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    print("\n--------------------------------------------------")
    repo_url = input("🔗 Cole o URL do seu repositório GitHub (ex: https://github.com/allvita07/meu-app.git): ").strip()
    token = input("🔑 Cole o seu Token do GitHub (Personal Access Token): ").strip()
    print("--------------------------------------------------")

    if not repo_url or not token:
        print("⚠️ URL ou Token em falta.")
        sys.exit(0)

    if "https://" in repo_url:
        auth_url = repo_url.replace("https://", f"https://{token}@")
    else:
        auth_url = f"https://{token}@{repo_url}"

    subprocess.run(["git", "remote", "remove", "origin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", auth_url], check=True)

    print("🚀 A enviar código para o GitHub...")
    res = subprocess.run(["git", "push", "-f", "-u", "origin", "main"])

    if res.returncode == 0:
        print("\n🎉 ENVIADO COM SUCESSO!")
        print("💡 Abra o GitHub na aba 'Actions' — a compilação do APK vai correr de forma limpa na nuvem!")
    else:
        print("\n❌ Erro no envio. Confirme se o URL e o Token estão corretos.")

except Exception as e:
    print(f"\n❌ Erro crítico: {e}")

