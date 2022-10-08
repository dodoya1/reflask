"""
マルコフ連鎖で文章を生成する

License: MIT
Created at: 2021/03/02
"""
# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer 
import random


class MarkovChain:
    def analyze(self, text):
        """
        textを解析しマルコフ連鎖を行う
        """
        t = Tokenizer()
        toks = list(t.tokenize(text))  # textを形態素解析
        matrix = self.create_matrix(toks)  # toksから行列を生成
        return self.markov(matrix)  # 行列を使ってマルコフ連鎖を行う

    def create_matrix(self, toks):
        """
        toksからマルコフ連鎖に使う行列を生成する
        """
        mat = []
        i = 0

        while i < len(toks) - 2:
            t1 = toks[i]
            t2 = toks[i + 1]
            t3 = toks[i + 2]
            mat.append((t1, t2, t3))
            i += 1

        return mat

    def markov(self, mat):
        """
        matを使ってマルコフ連鎖を行いテキストを生成する
        """
        toks = self.find_start_toks(mat)  # 最初のトークン列を探す
        if toks is None:
            return None

        s = self.toks_to_text(toks)
        before_selected = None  # 1つ前の選択したトークン列

        while True:
            candidates = self.grep_candidates(mat, toks)
            if not len(candidates):  # 候補が見つからない
                if s[-1] != '。':
                    s += '。'
                return s

            # 候補から次につなげるトークン列を選ぶ
            selected = self.random_choice(before_selected, candidates)
            s += self.toks_to_text(selected)  # トークン列をテキストに
            if selected[1].surface == '。':  # 終了条件
                break

            before_selected = selected
            toks = selected

        return s

    def random_choice(self, before_selected, candidates):
        """
        candidatesからランダムに1つ選択する
        """
        while True:
            selected = random.choice(candidates)
            if before_selected is None:
                break
            # 同じトークン列が続かないようにここで1つ前のトークン列と比較しておく
            if before_selected[0].surface != selected[0].surface or \
               before_selected[1].surface != selected[1].surface:
                break
        return selected

    def grep_candidates(self, mat, toks):
        """
        matから候補をリストアップする
        """
        candidate = []

        for row in mat:
            if row[0].surface == toks[1].surface:
                candidate.append(row[1:])

        return candidate

    def find_start_toks(self, mat):
        """
        matから開始トークン列を返す
        """
        if not len(mat):
            return None

        return mat[0][:2]

    def toks_to_text(self, toks):
        """
        toksをテキストにする
        """
        s = ''
        for tok in toks:
            s += tok.surface
        return s

def main():
    #夏目漱石「吾輩は猫である」をテキストとして与える。
    text = '''吾輩は猫である。名前はまだ無い。どこで生れたかとんと見当がつかぬ。何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。吾輩はここで始めて人間というものを見た。しかもあとで聞くとそれは書生という人間中で一番獰悪な種族であったそうだ。この書生というのは時々我々を捕えて煮て食うという話である。しかしその当時は何という考もなかったから別段恐しいとも思わなかった。ただ彼の掌に載せられてスーと持ち上げられた時何だかフワフワした感じがあったばかりである。掌の上で少し落ちついて書生の顔を見たのがいわゆる人間というものの見始であろう。この時妙なものだと思った感じが今でも残っている。第一毛をもって装飾されべきはずの顔がつるつるしてまるで薬缶だ。その後猫にもだいぶ逢ったがこんな片輪には一度も出会わした事がない。のみならず顔の真中があまりに突起している。そうしてその穴の中から時々ぷうぷうと煙を吹く。どうも咽せぽくて実に弱った。これが人間の飲む煙草というものである事はようやくこの頃知った。'''
    m = MarkovChain()
    result = m.analyze(text)
    return result