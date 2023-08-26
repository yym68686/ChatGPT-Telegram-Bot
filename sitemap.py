import itertools
import re
from typing import Any, Callable, Generator, Iterable, List, Optional

# from langchain.document_loaders.web_base import WebBaseLoader
from langchain.schema import Document


def _default_parsing_function(content: Any) -> str:
    return str(content.get_text())


def _default_meta_function(meta: dict, _content: Any) -> dict:
    return {"source": meta["loc"], **meta}


def _batch_block(iterable: Iterable, size: int) -> Generator[List[dict], None, None]:
    it = iter(iterable)
    while item := list(itertools.islice(it, size)):
        yield item

"""Web base loader class."""
import asyncio
import logging
import warnings
from typing import Any, Dict, Iterator, List, Optional, Union

import aiohttp
import requests

from langchain.docstore.document import Document


logger = logging.getLogger(__name__)

default_header_template = {
    "User-Agent": "",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*"
    ";q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def _build_metadata(soup: Any, url: str) -> dict:
    """Build metadata from BeautifulSoup output."""
    metadata = {"source": url}
    if title := soup.find("title"):
        metadata["title"] = title.get_text()
    if description := soup.find("meta", attrs={"name": "description"}):
        metadata["description"] = description.get("content", "No description found.")
    if html := soup.find("html"):
        metadata["language"] = html.get("lang", "No language found.")
    return metadata

# from langchain.document_loaders.base import BaseLoader

"""Abstract interface for document loader implementations."""
from abc import ABC, abstractmethod
from typing import Iterator, List, Optional

# from langchain.document_loaders.blob_loaders import Blob
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter


class BaseLoader(ABC):
    """Interface for Document Loader.

    Implementations should implement the lazy-loading method using generators
    to avoid loading all Documents into memory at once.

    The `load` method will remain as is for backwards compatibility, but its
    implementation should be just `list(self.lazy_load())`.
    """

    # Sub-classes should implement this method
    # as return list(self.lazy_load()).
    # This method returns a List which is materialized in memory.
    @abstractmethod
    def load(self) -> List[Document]:
        """Load data into Document objects."""

    def load_and_split(
        self, text_splitter: Optional[TextSplitter] = None
    ) -> List[Document]:
        """Load Documents and split into chunks. Chunks are returned as Documents.

        Args:
            text_splitter: TextSplitter instance to use for splitting documents.
              Defaults to RecursiveCharacterTextSplitter.

        Returns:
            List of Documents.
        """
        if text_splitter is None:
            _text_splitter: TextSplitter = RecursiveCharacterTextSplitter()
        else:
            _text_splitter = text_splitter
        docs = self.load()
        return _text_splitter.split_documents(docs)

    # Attention: This method will be upgraded into an abstractmethod once it's
    #            implemented in all the existing subclasses.
    def lazy_load(
        self,
    ) -> Iterator[Document]:
        """A lazy loader for Documents."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement lazy_load()"
        )

class WebBaseLoader(BaseLoader):
    """Load HTML pages using `urllib` and parse them with `BeautifulSoup'."""

    web_paths: List[str]

    requests_per_second: int = 2
    """Max number of concurrent requests to make."""

    default_parser: str = "html.parser"
    """Default parser to use for BeautifulSoup."""

    requests_kwargs: Dict[str, Any] = {}
    """kwargs for requests"""

    raise_for_status: bool = False
    """Raise an exception if http status code denotes an error."""

    bs_get_text_kwargs: Dict[str, Any] = {}
    """kwargs for beatifulsoup4 get_text"""

    def __init__(
        self,
        web_path: Union[str, List[str]],
        header_template: Optional[dict] = None,
        verify_ssl: Optional[bool] = True,
        proxies: Optional[dict] = None,
        continue_on_failure: Optional[bool] = False,
    ):
        """Initialize with webpage path."""

        # TODO: Deprecate web_path in favor of web_paths, and remove this
        # left like this because there are a number of loaders that expect single
        # urls
        if isinstance(web_path, str):
            self.web_paths = [web_path]
        elif isinstance(web_path, List):
            self.web_paths = web_path

        try:
            import bs4  # noqa:F401
        except ImportError:
            raise ImportError(
                "bs4 package not found, please install it with " "`pip install bs4`"
            )

        headers = header_template or default_header_template
        if not headers.get("User-Agent"):
            try:
                from fake_useragent import UserAgent

                headers["User-Agent"] = UserAgent().random
            except ImportError:
                logger.info(
                    "fake_useragent not found, using default user agent."
                    "To get a realistic header for requests, "
                    "`pip install fake_useragent`."
                )

        self.session = requests.Session()
        self.session.headers = dict(headers)
        self.session.verify = verify_ssl
        self.continue_on_failure = continue_on_failure

        if proxies:
            self.session.proxies.update(proxies)

    @property
    def web_path(self) -> str:
        if len(self.web_paths) > 1:
            raise ValueError("Multiple webpaths found.")
        return self.web_paths[0]

    async def _fetch(
        self, url: str, retries: int = 3, cooldown: int = 2, backoff: float = 1.5
    ) -> str:
        async with aiohttp.ClientSession() as session:
            for i in range(retries):
                try:
                    async with session.get(
                        url,
                        headers=self.session.headers,
                        ssl=None if self.session.verify else False,
                    ) as response:
                        return await response.text()
                except aiohttp.ClientConnectionError as e:
                    if i == retries - 1:
                        raise
                    else:
                        logger.warning(
                            f"Error fetching {url} with attempt "
                            f"{i + 1}/{retries}: {e}. Retrying..."
                        )
                        await asyncio.sleep(cooldown * backoff**i)
        raise ValueError("retry count exceeded")

    async def _fetch_with_rate_limit(
        self, url: str, semaphore: asyncio.Semaphore
    ) -> str:
        async with semaphore:
            try:
                return await self._fetch(url)
            except Exception as e:
                if self.continue_on_failure:
                    logger.warning(
                        f"Error fetching {url}, skipping due to"
                        f" continue_on_failure=True"
                    )
                    return ""
                logger.exception(
                    f"Error fetching {url} and aborting, use continue_on_failure=True "
                    "to continue loading urls after encountering an error."
                )
                raise e

    async def fetch_all(self, urls: List[str]) -> Any:
        """Fetch all urls concurrently with rate limiting."""
        semaphore = asyncio.Semaphore(self.requests_per_second)
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(self._fetch_with_rate_limit(url, semaphore))
            tasks.append(task)
        try:
            from tqdm.asyncio import tqdm_asyncio

            return await tqdm_asyncio.gather(
                *tasks, desc="Fetching pages", ascii=True, mininterval=1
            )
        except ImportError:
            warnings.warn("For better logging of progress, `pip install tqdm`")
            return await asyncio.gather(*tasks)

    @staticmethod
    def _check_parser(parser: str) -> None:
        """Check that parser is valid for bs4."""
        valid_parsers = ["html.parser", "lxml", "xml", "lxml-xml", "html5lib"]
        if parser not in valid_parsers:
            raise ValueError(
                "`parser` must be one of " + ", ".join(valid_parsers) + "."
            )

    async def scrape_all(self, urls: List[str], parser: Union[str, None] = None) -> List[Any]:
        """Fetch all urls, then return soups for all results."""
        from bs4 import BeautifulSoup

        results = await self.fetch_all(urls)
        final_results = []
        for i, result in enumerate(results):
            url = urls[i]
            if parser is None:
                if url.endswith(".xml"):
                    parser = "xml"
                else:
                    parser = self.default_parser
                self._check_parser(parser)
            final_results.append(BeautifulSoup(result, parser))

        return final_results

    def _scrape(self, url: str, parser: Union[str, None] = None) -> Any:
        from bs4 import BeautifulSoup

        if parser is None:
            if url.endswith(".xml"):
                parser = "xml"
            else:
                parser = self.default_parser

        self._check_parser(parser)

        html_doc = self.session.get(url, **self.requests_kwargs)
        if self.raise_for_status:
            html_doc.raise_for_status()
        html_doc.encoding = html_doc.apparent_encoding
        return BeautifulSoup(html_doc.text, parser)

    def scrape(self, parser: Union[str, None] = None) -> Any:
        """Scrape data from webpage and return it in BeautifulSoup format."""

        if parser is None:
            parser = self.default_parser

        return self._scrape(self.web_path, parser)

    def lazy_load(self) -> Iterator[Document]:
        """Lazy load text from the url(s) in web_path."""
        for path in self.web_paths:
            soup = self._scrape(path)
            text = soup.get_text(**self.bs_get_text_kwargs)
            metadata = _build_metadata(soup, path)
            yield Document(page_content=text, metadata=metadata)

    def load(self) -> List[Document]:
        """Load text from the url(s) in web_path."""
        return list(self.lazy_load())

    def aload(self) -> List[Document]:
        """Load text from the urls in web_path async into Documents."""

        results = self.scrape_all(self.web_paths)
        docs = []
        for i in range(len(results)):
            soup = results[i]
            text = soup.get_text(**self.bs_get_text_kwargs)
            metadata = _build_metadata(soup, self.web_paths[i])
            docs.append(Document(page_content=text, metadata=metadata))

        return docs

class SitemapLoader(WebBaseLoader):
    """Load a sitemap and its URLs."""

    def __init__(
        self,
        web_path: str,
        filter_urls: Optional[List[str]] = None,
        parsing_function: Optional[Callable] = None,
        blocksize: Optional[int] = None,
        blocknum: int = 0,
        meta_function: Optional[Callable] = None,
        is_local: bool = False,
        continue_on_failure: bool = False,
    ):
        """Initialize with webpage path and optional filter URLs.

        Args:
            web_path: url of the sitemap. can also be a local path
            filter_urls: list of strings or regexes that will be applied to filter the
                urls that are parsed and loaded
            parsing_function: Function to parse bs4.Soup output
            blocksize: number of sitemap locations per block
            blocknum: the number of the block that should be loaded - zero indexed.
                Default: 0
            meta_function: Function to parse bs4.Soup output for metadata
                remember when setting this method to also copy metadata["loc"]
                to metadata["source"] if you are using this field
            is_local: whether the sitemap is a local file. Default: False
            continue_on_failure: whether to continue loading the sitemap if an error
                occurs loading a url, emitting a warning instead of raising an
                exception. Setting this to True makes the loader more robust, but also
                may result in missing data. Default: False
        """

        if blocksize is not None and blocksize < 1:
            raise ValueError("Sitemap blocksize should be at least 1")

        if blocknum < 0:
            raise ValueError("Sitemap blocknum can not be lower then 0")

        try:
            import lxml  # noqa:F401
        except ImportError:
            raise ImportError(
                "lxml package not found, please install it with " "`pip install lxml`"
            )

        super().__init__(web_path)

        self.filter_urls = filter_urls
        self.parsing_function = parsing_function or _default_parsing_function
        self.meta_function = meta_function or _default_meta_function
        self.blocksize = blocksize
        self.blocknum = blocknum
        self.is_local = is_local
        self.continue_on_failure = continue_on_failure

    async def parse_sitemap(self, soup: Any) -> List[dict]:
        """Parse sitemap xml and load into a list of dicts.

        Args:
            soup: BeautifulSoup object.

        Returns:
            List of dicts.
        """
        els = []
        for url in soup.find_all("url"):
            loc = url.find("loc")
            if not loc:
                continue

            # Strip leading and trailing whitespace and newlines
            loc_text = loc.text.strip()

            if self.filter_urls and not any(
                re.match(r, loc_text) for r in self.filter_urls
            ):
                continue

            els.append(
                {
                    tag: prop.text
                    for tag in ["loc", "lastmod", "changefreq", "priority"]
                    if (prop := url.find(tag))
                }
            )

        for sitemap in soup.find_all("sitemap"):
            loc = sitemap.find("loc")
            if not loc:
                continue
            soup_child = await self.scrape_all([loc.text], "xml")[0]

            els.extend(self.parse_sitemap(soup_child))
        return els

    async def load(self) -> List[Document]:
        """Load sitemap."""
        if self.is_local:
            try:
                import bs4
            except ImportError:
                raise ImportError(
                    "beautifulsoup4 package not found, please install it"
                    " with `pip install beautifulsoup4`"
                )
            fp = open(self.web_path)
            soup = bs4.BeautifulSoup(fp, "xml")
        else:
            soup = self.scrape("xml")

        els = await self.parse_sitemap(soup)

        if self.blocksize is not None:
            elblocks = list(_batch_block(els, self.blocksize))
            blockcount = len(elblocks)
            if blockcount - 1 < self.blocknum:
                raise ValueError(
                    "Selected sitemap does not contain enough blocks for given blocknum"
                )
            else:
                els = elblocks[self.blocknum]

        results = await self.scrape_all([el["loc"].strip() for el in els if "loc" in el])

        return [
            Document(
                page_content=self.parsing_function(results[i]),
                metadata=self.meta_function(els[i], results[i]),
            )
            for i in range(len(results))
        ]
