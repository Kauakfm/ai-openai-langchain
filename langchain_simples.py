from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
import os

numero_de_dias = 7
numero_de_criancas = 2
atividade= "praia"

modelo_do_prompt = PromptTemplate.from_template(
  "Crie um roteiro de viagem de {dias} dias, para uma familia com {criancas} crianças que gostam de {atividade}"
)

modelo_restaurantes = ChatPromptTemplate.from_template(
  "Sugira restaurantes populares entre locais em {cidade}"
)

modelo_cultural  = ChatPromptTemplate.from_template(
  "Sugira atividades e locais culturais em {cidade}"
)

prompt = modelo_do_prompt.format(dias=numero_de_dias,
                        criancas=numero_de_criancas,
                        atividade=atividade)

print(prompt)

llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.5,
  max_completion_tokens=50,
  api_key=os.getenv("OPENAI_API_KEY")
)

resposta = llm.invoke(prompt)
print(resposta.content)
