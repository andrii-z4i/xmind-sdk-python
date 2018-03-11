from xmind.core import const
from xmind.tests import logging_configuration as lc
from xmind.tests import base


class ConstTest(base.Base):
    """ConstTest"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('ConstTest')
        return self._logger

    def test_all_const_values(self):

        self.assertEqual(const.XMIND_EXT, ".xmind")

        self.assertEqual(const.VERSION, "2.0")
        self.assertEqual(const.NAMESPACE, "xmlns")
        self.assertEqual(const.XMAP, "urn:xmind:xmap:xmlns:content:2.0")

        self.assertEqual(const.ATTACHMENTS_DIR, "attachments/")
        self.assertEqual(const.MARKERS_DIR, "markers/")
        self.assertEqual(const.META_INF_DIR, "META-INF/")
        self.assertEqual(const.REVISIONS_DIR, "Revisions/")

        self.assertEqual(const.CONTENT_XML, "content.xml")
        self.assertEqual(const.STYLES_XML, "styles.xml")
        self.assertEqual(const.META_XML, "meta.xml")
        self.assertEqual(const.MANIFEST_XML, "META-INF/manifest.xml")
        self.assertEqual(const.MARKER_SHEET_XML, "markerSheet.xml")
        self.assertEqual(const.MARKER_SHEET,
                         (const.MARKERS_DIR + const.MARKER_SHEET_XML))
        self.assertEqual(const.REVISIONS_XML, "revisions.xml")

        self.assertEqual(const.TAG_WORKBOOK, "xmap-content")
        self.assertEqual(const.TAG_TOPIC, "topic")
        self.assertEqual(const.TAG_TOPICS, "topics")
        self.assertEqual(const.TAG_SHEET, "sheet")
        self.assertEqual(const.TAG_TITLE, "title")
        self.assertEqual(const.TAG_POSITION, "position")
        self.assertEqual(const.TAG_CHILDREN, "children")
        self.assertEqual(const.TAG_NOTES, "notes")
        self.assertEqual(const.TAG_RELATIONSHIP, "relationship")
        self.assertEqual(const.TAG_RELATIONSHIPS, "relationships")
        self.assertEqual(const.TAG_MARKERREFS, "marker-refs")
        self.assertEqual(const.TAG_MARKERREF, "marker-ref")
        self.assertEqual(const.ATTR_VERSION, "version")
        self.assertEqual(const.ATTR_ID, "id")
        self.assertEqual(const.ATTR_STYLE_ID, "style-id")
        self.assertEqual(const.ATTR_TIMESTAMP, "timestamp")
        self.assertEqual(const.ATTR_THEME, "theme")
        self.assertEqual(const.ATTR_X, "svg:x")
        self.assertEqual(const.ATTR_Y, "svg:y")
        self.assertEqual(const.ATTR_HREF, "xlink:href")
        self.assertEqual(const.ATTR_BRANCH, "branch")
        self.assertEqual(const.ATTR_TYPE, "type")
        self.assertEqual(const.ATTR_END1, "end1")
        self.assertEqual(const.ATTR_END2, "end2")
        self.assertEqual(const.ATTR_MARKERID, "marker-id")

        self.assertEqual(const.NS_URI, "http://www.w3.org/1999/xhtml")

        self.assertEqual(const.NS_XHTML, (const.NS_URI,
                                          "xhtml", "http://www.w3.org/1999/xhtml"))
        self.assertEqual(const.NS_XHTML, (const.NS_URI,
                                          "xhtml", "http://www.w3.org/1999/xhtml"))
        self.assertEqual(const.NS_XLINK, (const.NS_URI,
                                          "xlink", "http://www.w3.org/1999/xlink"))
        self.assertEqual(const.NS_SVG, (const.NS_URI, "svg",
                                        "http://www.w3.org/2000/svg"))
        self.assertEqual(const.NS_FO, (const.NS_URI, "fo",
                                       "http://www.w3.org/1999/XSL/Format"))

        self.assertEqual(const.VAL_FOLDED, "folded")

        self.assertEqual(const.TOPIC_ROOT, "root")
        self.assertEqual(const.TOPIC_ATTACHED, "attached")

        self.assertEqual(const.FILE_PROTOCOL, "file://")
        self.assertEqual(const.TOPIC_PROTOCOL, "xmind:#")
        self.assertEqual(const.HTTP_PROTOCOL, "http://")
        self.assertEqual(const.HTTPS_PROTOCOL, "https://")

        self.assertEqual(const.HTML_FORMAT_NOTE, "html")
        self.assertEqual(const.PLAIN_FORMAT_NOTE, "plain")
