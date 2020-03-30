from structure import Trie


def test_trie():
    """测试以下字典树:
    ```
    N   N          N              N
       a       d   a   e      d   a   e
              d f     c f    d *f*  *c* f
                 g   h          g   h
    ```

      - 空
      - 只有一个字符
      - 所有字符串都是到叶子节点才终止
      - 部分字符串到非叶子节点终止 (用 ** 标记)
    """
    words_set = (
        set(),
        {'a'},
        {'dd', 'dfg', 'a', 'ech', 'ef'},
        {'dd', 'df', 'dfg', 'a', 'ec', 'ech', 'ef'},
    )

    for words in words_set:
        trie = Trie.from_iterable(words)
        assert set(trie) == set(words)
        assert len(trie) == len(words)

        # 添加重复的元素应该没有任何影响
        for word in words:
            trie.add(word)
        assert len(trie) == len(words)

        for word in words:
            for i in range(1, len(word) + 1):
                # 字符串的子串如果不是一个单词, 那么就不应该在 `trie` 中.
                if i < len(word) and word[:i] not in words:
                    assert word[:i] not in trie
                else:
                    assert word[:i] in trie

                # 所有子串都是前缀.
                assert trie.startswith(word[:i])
