from langchain_openai import ChatOpenAI
from langchain.globals import set_debug
from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from operator import itemgetter
import os

set_debug(True)


class Destino(BaseModel):
  cidade = Field("cidade a visitar")
  motivo = Field("motivo pelo qual é interessante visitar essa cidade")

llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0.5,
  api_key=os.getenv("OPENAI_API_KEY")
)

parseador = JsonOutputParser(pydantic_object=Destino)

modelo_cidade = PromptTemplate(
  template="""Sugira uma cidade dado meu interesse por {interesses}.
  {formatacao_de_saida}
  """, 
  input_variables=["interesses"],
  partial_variables={"formatacao_de_saida": parseador.get_format_instructions()}
)

modelo_restaurantes = ChatPromptTemplate.from_template(
  "Sugira restaurantes populares entre locais em {cidade}"
)

modelo_cultural  = ChatPromptTemplate.from_template(
  "Sugira atividades e locais culturais em {cidade}"
)

modelo_final = ChatPromptTemplate.from_messages(
  [
  ("ai",  "Sugestão de viagem para a cidade: {cidade}"),
  ("ai",  "Restaurantes que você não pode perder: {restaurantes}"),
  ("ai",  "Atividades e locais culturais recomendados: {locais_culturais}"),
  ("system",  "Combine as informaçoes anteriores em 2 parágrafos coerentes."),
  ]
)

parte1 = modelo_cidade | llm | parseador
parte2 = modelo_restaurantes | llm | StrOutputParser()
parte3 = modelo_cultural | llm | StrOutputParser()
parte4 = modelo_final | llm | StrOutputParser()

cadeia = (parte1 | {
    "restaurantes": parte2, 
    "locais_culturais": parte3,
    "cidade": itemgetter("cidade")
} 
| parte4)
#print(modelo_cidade.invoke({"interesses" : "praias"}))

resultado = cadeia.invoke({"interesses" : "praias"})
print(resultado)

