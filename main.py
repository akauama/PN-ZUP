from agents.logo_maker import run_logo_maker

def main():
    print("🚀 Iniciando aplicação principal...")
    prompt = input("Digite a descrição da logomarca: ")
    resultado = run_logo_maker({"logo_prompt_for_ai": prompt})

    if resultado["logo_image_url"]:
        print("\n✅ Logomarca gerada com sucesso!")
        print("URL da imagem:", resultado["logo_image_url"])
        print("Markdown:", resultado["logo_image_markdown"])
    else:
        print("\n⚠️ Erro:", resultado["notes"])


if __name__ == "__main__":
    main()
