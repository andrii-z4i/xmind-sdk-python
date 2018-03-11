from xmind.tests import logging_configuration as lc
from xmind.core.relationship import RelationshipsElement
from xmind.tests import base
from xmind.core.const import TAG_RELATIONSHIPS


class TestRelationshipsElement(base.Base):
    """Test class for RelationshipsElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('relationshipsElement')
        return self._logger

    def test_init(self):
        _wb_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.relationship.WorkbookMixinElement.__init__', autospec=True)

        _obj1 = RelationshipsElement()
        _wb_mixin_element_init.assert_called_with(_obj1, None, None)
        self.assertEqual(_obj1.TAG_NAME, TAG_RELATIONSHIPS)

        _obj2 = RelationshipsElement(1)
        _wb_mixin_element_init.assert_called_with(_obj2, 1, None)
        self.assertEqual(_obj2.TAG_NAME, TAG_RELATIONSHIPS)

        _obj3 = RelationshipsElement(1, 2)
        _wb_mixin_element_init.assert_called_with(_obj3, 1, 2)
        self.assertEqual(_obj3.TAG_NAME, TAG_RELATIONSHIPS)

        _obj4 = RelationshipsElement(node=None, ownerWorkbook=1)
        _wb_mixin_element_init.assert_called_with(_obj4, None, 1)
        self.assertEqual(_obj4.TAG_NAME, TAG_RELATIONSHIPS)

        with self.assertRaises(TypeError) as _ex:
            RelationshipsElement(1, 2, 3)

        self.assertTrue(_ex.exception.args[0].find("__init__() takes") != -1)
        # 4 because for last case we don't get to __init__ of super
        self.assertEqual(_wb_mixin_element_init.call_count, 4)
