#!/usr/bin/env python
# coding: utf-8

# インデックスの作成
from llama_index import GPTVectorStoreIndex, ServiceContext, LLMPredictor, JSONReader
from langchain.chat_models import ChatOpenAI
import os
import sys


def create_index(source_json: str, index_file: str):
  documents = JSONReader().load_data(source_json)
  # gpt-3.5-turbo を指定（現状デフォルトは davinci ）
  service_context = ServiceContext.from_defaults(
    llm_predictor=LLMPredictor(llm=ChatOpenAI(model_name="gpt-3.5-turbo")))
  # documents をもとに Embeddings API を通信してベクター取得し GPTSimpleVectorIndex を生成
  index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
  # save to disk
  index.storage_context.persist(index_file)


if __name__ == '__main__':
  if 'OPENAI_API_KEY' not in os.environ:
    print('Error: OPENAI_API_KEYを指定してください', file=sys.stderr)
    sys.exit(1)
  create_index('data/cw_faq.json', 'data/index')
