#!/usr/bin/env python
# coding: utf-8

from llama_index import load_index_from_storage, StorageContext
from llama_index.prompts.prompts import RefinePrompt, QuestionAnswerPrompt

# デバッグログの出力
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)


def chat_with_gpt(question: str, index_dir: str):
  # インデックスをファイルから読み込む
  storage_context = StorageContext.from_defaults(persist_dir=index_dir)
  index = load_index_from_storage(storage_context)

  # テンプレートの作成
  qa_prompt_tmpl = (
    "私たちは以下の情報をコンテキスト情報として与えます。 \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "あなたはAIとして、この情報をもとに質問を日本語で答えます。回答にはURLを含めてください。前回と同じ回答の場合は同じ回答を行います。: {query_str}\n"
  )
  qa_prompt = QuestionAnswerPrompt(qa_prompt_tmpl)
  refine_prompt = ("元の質問は次のとおりです: {query_str} \n"
                   "既存の回答を提供しました: {existing_answer} \n"
                   "既存の答えを洗練する機会があります \n"
                   "(必要な場合のみ)以下にコンテキストを追加します。 \n"
                   "------------\n"
                   "{context_msg}\n"
                   "------------\n"
                   "新しいコンテキストを考慮して、元の答えをより良く洗練して質問に答えてください。\n"
                   "コンテキストが役に立たない場合は、元の回答と同じものを返します。回答にはURLを含めてください。")
  refine_prompt = RefinePrompt(refine_prompt)

  # ベクター検索 + Chat Completion API 実行
  query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
    refine_template=refine_prompt,
  )
  response = query_engine.query(question)
  return response.response


if __name__ == '__main__':
  print(chat_with_gpt('パスワードを忘れた', 'data/index'))
