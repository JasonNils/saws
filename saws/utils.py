# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import six
import shlex
import fuzzyfinder
from prompt_toolkit.completion import Completion


class TextUtils(object):
    """Utilities for parsing and matching text.

    Attributes:
        * None.
    """

    def shlex_split(self, text):
        """Wrapper for shlex, because it does not seem to handle unicode in 2.6.

        Args:
            * text: A string to split.

        Returns:
            A list that contains words for each split element of text.
        """
        if six.PY2:
            text = text.encode('utf-8')
        return shlex.split(text)

    def find_collection_matches(self, word, collection, fuzzy):
        """Yields all matching names in list.

        Args:
            * word: A string representing the word before
                the cursor.
            * collection: A collection of words to match.
            * fuzzy: A boolean that specifies whether to use fuzzy matching.

        Yields:
            A generator of prompt_toolkit's Completions.
        """
        if fuzzy:
            for suggestion in fuzzyfinder.fuzzyfinder(word, collection):
                yield Completion(suggestion, -len(word))
        else:
            for name in sorted(collection):
                if name.startswith(word) or not word:
                    yield Completion(name, -len(word))

    def find_matches(self, word, collection, fuzzy):
        """Finds all matches in collection for word.

        Args:
            * word: A string representing the word before
                the cursor.
            * collection: A collection of words to match.
            * fuzzy: A boolean that specifies whether to use fuzzy matching.

        Yields:
            A generator of prompt_toolkit's Completions.
        """
        word = self.last_token(word).lower()
        for suggestion in self.find_collection_matches(
                word, collection, fuzzy):
            yield suggestion

    def get_tokens(self, text):
        """Parses out all tokens.

        Args:
            * text: A string to split into tokens.

        Returns:
            A list of strings for each word in the text.
        """
        if text is not None:
            text = text.strip()
            words = self.safe_split(text)
            return words
        return []

    def last_token(self, text):
        """Finds the last word in text.

        Args:
            * text: A string to parse and obtain the last word.

        Returns:
            A string representing the last word in the text.
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = self.safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

    def safe_split(self, text):
        """Safely splits the input text.

        Shlex can't always split. For example, "\" crashes the completer.

        Args:
            * text: A string to split.

        Returns:
            A list that contains words for each split element of text.

        """
        try:
            words = self.shlex_split(text)
            return words
        except:
            return text
