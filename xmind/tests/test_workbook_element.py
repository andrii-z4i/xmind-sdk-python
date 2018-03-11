from xmind.tests import logging_configuration as lc
from xmind.tests import base
from unittest.mock import patch, MagicMock, call, Mock
from xmind.core.workbook import WorkbookElement
from xmind.core.const import TAG_WORKBOOK, NAMESPACE, XMAP, NS_FO, NS_XHTML, NS_XLINK, NS_SVG, TAG_SHEET, ATTR_VERSION


class TestWorkbookElement(base.Base):

    def setUp(self):
        super(TestWorkbookElement, self).setUp()

        self._workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.workbook.WorkbookMixinElement.__init__')
        self._getSheets = self._init_patch_with_name('_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
                                                     return_value=True)
        self._setAttributeNS = self._init_patch_with_name(
            '_setAttributeNS', 'xmind.core.Element.setAttributeNS')
        self._owner_workbook = MagicMock()
        self._updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.workbook.WorkbookMixinElement.updateModifiedTime')

    def _assert_init_methods_called(self):
        self._workbook_mixin_element_init.assert_called_once_with(None, None)
        self.assertListEqual([
            call((NAMESPACE, XMAP), NS_FO),
            call((NAMESPACE, XMAP), NS_XHTML),
            call((NAMESPACE, XMAP), NS_XLINK),
            call((NAMESPACE, XMAP), NS_SVG)], self._setAttributeNS.call_args_list)
        self._getSheets.assert_called_once_with()

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('TestWoorkbookElement')
        return self._logger

    def test_excessive_parameters(self):
        _parameters = [
            ('setOwnerWorkbook', 1),
            ('getSheets', 0),
            ('getSheetByIndex', 1),
            ('createSheet', 0),
            ('addSheet', 2),
            ('removeSheet', 1),
            ('moveSheet', 2),
            ('getVersion', 0),
            ('__init__', (2, False))
        ]

        _test_el = WorkbookElement()
        self._assert_init_methods_called()
        self._remove_patched_function('_getSheets')

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _test_el)

    def test_WorkbookElement_init_is_getSheet(self):
        self._remove_patched_function('_getSheets')
        _getSheets = self._init_patch_with_name('_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
                                                return_value=True, autospec=True)
        _createSheet = self._init_patch_with_name(
            '_createSheet', 'xmind.core.workbook.WorkbookElement.createSheet', autospec=True)
        _addSheet = self._init_patch_with_name(
            '_addSheet', 'xmind.core.workbook.WorkbookElement.addSheet', autospec=True)

        _test_el = WorkbookElement()

        self.assertEqual(_test_el.TAG_NAME, TAG_WORKBOOK)
        self.assertListEqual([
            call((NAMESPACE, XMAP), NS_FO),
            call((NAMESPACE, XMAP), NS_XHTML),
            call((NAMESPACE, XMAP), NS_XLINK),
            call((NAMESPACE, XMAP), NS_SVG)], self._setAttributeNS.call_args_list)
        _getSheets.assert_called_once_with(_test_el)
        _createSheet.assert_not_called()
        _addSheet.assert_not_called()
        self._workbook_mixin_element_init.assert_called_once_with(None, None)

    def test_WorkbookElement_init_no_getSheet(self):
        self._remove_patched_function('_getSheets')

        _getSheets = self._init_patch_with_name('_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
                                                return_value=False, autospec=True)
        _createSheet = self._init_patch_with_name('_createSheet', 'xmind.core.workbook.WorkbookElement.createSheet',
                                                  return_value='sheet', autospec=True)
        _addSheet = self._init_patch_with_name(
            '_addSheet', 'xmind.core.workbook.WorkbookElement.addSheet', autospec=True)

        _test_el = WorkbookElement()

        self.assertEqual(_test_el.TAG_NAME, TAG_WORKBOOK)
        self.assertListEqual([
            call((NAMESPACE, XMAP), NS_FO),
            call((NAMESPACE, XMAP), NS_XHTML),
            call((NAMESPACE, XMAP), NS_XLINK),
            call((NAMESPACE, XMAP), NS_SVG)], self._setAttributeNS.call_args_list)
        _getSheets.assert_called_once_with(_test_el)
        _createSheet.assert_called_once_with(_test_el)
        _addSheet.assert_called_once_with(_test_el, 'sheet')
        self._workbook_mixin_element_init.assert_called_once_with(None, None)

    def test_WorkbookElement_init_called_with_diff_parameters(self):
        _test_el_1 = WorkbookElement('node1')
        self._workbook_mixin_element_init.assert_called_once_with(
            'node1', None)

        _test_el_2 = WorkbookElement(ownerWorkbook='workbook2')
        self._workbook_mixin_element_init.assert_called_with(None, 'workbook2')

        _test_el_3 = WorkbookElement('node3', 'workbook3')
        self._workbook_mixin_element_init.assert_called_with(
            'node3', 'workbook3')

        self.assertEqual(self._workbook_mixin_element_init.call_count, 3)

    def test_WorkbookElement_setOwnerWorkbook(self):
        _test_el = WorkbookElement()
        self._assert_init_methods_called()

        with self.assertRaises(Exception) as _ex:
            _test_el.setOwnerWorkbook('ownerbook')

        self.assertTrue(_ex.exception.args[0].find(
            "WorkbookDocument allowed only contains one WorkbookElement") == 0)

    def test_WorkbookElement_getSheet_sheets_is_none(self):
        _test_el = WorkbookElement()
        self._assert_init_methods_called()

        self._remove_patched_function('_getSheets')

        _getChildNodesByTagName = self._init_patch_with_name(
            '_getChildNodesByTagName', 'xmind.core.Node.getChildNodesByTagName', return_value=None, autospec=True)
        _getOwnerWorkbook = self._init_patch_with_name(
            '_getOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.getOwnerWorkbook',
            return_value=self._owner_workbook, autospec=True)

        with self.assertRaises(Exception) as _ex:
            _test_el.getSheets()

        _getChildNodesByTagName.assert_called_once_with(_test_el, TAG_SHEET)
        _getOwnerWorkbook.assert_called_once_with(_test_el)
        self.assertTrue(_ex.exception.args[0].find(
            "'NoneType' object is not iterable") != -1)

    def test_WorkbookElement_getSheet_is_sheets_ownerbook_none(self):
        _test_el = WorkbookElement()
        self._assert_init_methods_called()

        self._remove_patched_function('_getSheets')

        _getChildNodesByTagName = self._init_patch_with_name(
            '_getChildNodesByTagName', 'xmind.core.Node.getChildNodesByTagName', return_value=[11, 12, 13], autospec=True)
        _getOwnerWorkbook = self._init_patch_with_name(
            '_getOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.getOwnerWorkbook',
            return_value=None, autospec=True)

        with patch('xmind.core.workbook.SheetElement') as _sheet_element_constructor:
            _sheet_element_constructor.side_effect = ['a', 'b', 'c']

            _sheets = _test_el.getSheets()

        self._assert_init_methods_called()
        _getChildNodesByTagName.assert_called_once_with(_test_el, TAG_SHEET)
        _getOwnerWorkbook.assert_called_once_with(_test_el)
        self.assertListEqual([
            call(11, None),
            call(12, None),
            call(13, None)], _sheet_element_constructor.call_args_list)
        self.assertListEqual(_sheets, ['a', 'b', 'c'])

    def test_WorkbookElement_getSheet_is_sheets_is_ownerbook(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')

        _getChildNodesByTagName = self._init_patch_with_name(
            '_getChildNodesByTagName', 'xmind.core.Node.getChildNodesByTagName', return_value=[11, 12, 13], autospec=True)
        _getOwnerWorkbook = self._init_patch_with_name(
            '_getOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.getOwnerWorkbook',
            return_value='workbook', autospec=True)

        with patch('xmind.core.workbook.SheetElement') as _sheet_element_constructor:
            _sheet_element_constructor.side_effect = ['a', 'b', 'c']

            _sheets = _test_el.getSheets()

        self._assert_init_methods_called()
        _getChildNodesByTagName.assert_called_once_with(_test_el, TAG_SHEET)
        _getOwnerWorkbook.assert_called_once_with(_test_el)
        self.assertListEqual([
            call(11, 'workbook'),
            call(12, 'workbook'),
            call(13, 'workbook')], _sheet_element_constructor.call_args_list)
        self.assertListEqual(_sheets, ['a', 'b', 'c'])

    def test_WorkbookElement_getSheetByIndex_var_index(self):
        _test_el = WorkbookElement()

        self._remove_patched_function('_getSheets')
        with patch.object(_test_el, 'getSheets') as _getSheets:
            _getSheets.return_value = ['sheet1', 'sheet2', 'sheet3']

            _sheets1 = _test_el.getSheetByIndex(None)
            self.assertIsNone(_sheets1)

            _sheets2 = _test_el.getSheetByIndex(-1)
            self.assertIsNone(_sheets2)

            _sheets3 = _test_el.getSheetByIndex(3)
            self.assertIsNone(_sheets3)

            _sheets4 = _test_el.getSheetByIndex(4)
            self.assertIsNone(_sheets4)

        self.assertEqual(_getSheets.call_count, 4)
        self._assert_init_methods_called()

    def test_WorkbookElement_getSheetByIndex_index_within_len_sheets(self):
        _test_el = WorkbookElement()

        self._remove_patched_function('_getSheets')

        with patch.object(_test_el, 'getSheets') as _getSheets:
            _getSheets.return_value = ['sheet1', 'sheet2', 'sheet3']

            _sheets = _test_el.getSheetByIndex(2)

        _getSheets.assert_called_once_with()
        self.assertEqual(_sheets, 'sheet3')
        self._assert_init_methods_called()

    def test_WorkbookElement_createSheet_getOwnerWorkbook_is_None(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getOwnerWorkbook')
        self._remove_patched_function('_sheet_element_init')

        _getOwnerWorkbook = self._init_patch_with_name(
            '_getOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.getOwnerWorkbook',
            return_value=None, autospec=True)
        _sheet_element_constructor = self._init_patch_with_name(
            '_sheet_element_constructor', 'xmind.core.workbook.SheetElement',
            return_value='SheetElement')

        _sheet = _test_el.createSheet()

        _getOwnerWorkbook.assert_called_once_with(_test_el)
        _sheet_element_constructor.assert_called_once_with(None, None)
        self.assertEqual(_sheet, 'SheetElement')
        self._assert_init_methods_called()

    def test_WorkbookElement_createSheet_is_getOwnerWorkbook(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getOwnerWorkbook')
        self._remove_patched_function('_sheet_element_init')

        _getOwnerWorkbook = self._init_patch_with_name(
            '_getOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.getOwnerWorkbook',
            return_value='workbook', autospec=True)
        _sheet_element_constructor = self._init_patch_with_name(
            '_sheet_element_constructor', 'xmind.core.workbook.SheetElement',
            return_value='SheetElement')

        _sheet = _test_el.createSheet()

        _getOwnerWorkbook.assert_called_once_with(_test_el)
        _sheet_element_constructor.assert_called_once_with(None, 'workbook')
        self.assertEqual(_sheet, 'SheetElement')
        self._assert_init_methods_called()

    def test_WorkbookElement_addSheet_index_goes_if(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_appendChild')
        self._remove_patched_function('_updateModifiedTime')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet3'], autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _insertBefore = self._init_patch_with_name(
            '_insertBefore', 'xmind.core.Node.insertBefore', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result1 = _test_el.addSheet('sheet')
        _result2 = _test_el.addSheet('sheet', -1)
        _result3 = _test_el.addSheet('sheet', 3)
        _result4 = _test_el.addSheet('sheet', 4)

        self.assertListEqual(_getSheets.call_args_list, [call(_test_el)]*4)
        self.assertListEqual(_appendChild.call_args_list,
                             [call(_test_el, 'sheet')]*4)
        _insertBefore.assert_not_called()
        self.assertEqual(_updateModifiedTime.call_count, 4)
        self._assert_init_methods_called()

    def test_WorkbookElement_addSheet_index_is_within_len_sheets(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_appendChild')
        self._remove_patched_function('_updateModifiedTime')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet3'], autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _insertBefore = self._init_patch_with_name(
            '_insertBefore', 'xmind.core.Node.insertBefore', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result = _test_el.addSheet('sheet', 0)

        _getSheets.assert_called_once_with(_test_el)
        _appendChild.assert_not_called()
        _insertBefore.assert_called_once_with(_test_el, 'sheet', 'sheet1')
        _updateModifiedTime.assert_called_once_with(_test_el)
        self._assert_init_methods_called()

    def test_WorkbookElement_removeSheet_len_sheets_less_or_equal_1(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=[[], ['sheet1']], autospec=True, return_value_as_side_effect=True)
        _getImplementation = self._init_patch_with_name(
            '_getImplementation', 'xmind.core.Node.getImplementation',
            return_value='implementation', autospec=True)
        _sheet = Mock()
        with patch.object(_sheet, 'getParentNode') as _getParentNode:
            _getParentNode.return_value = 'not equal'

            _result1 = _test_el.removeSheet(_sheet)
            self.assertIsNone(_result1)
            _result2 = _test_el.removeSheet(_sheet)
            self.assertIsNone(_result2)

        self.assertListEqual(_getSheets.call_args_list, [call(_test_el)]*2)
        _getParentNode.assert_not_called()
        _getImplementation.assert_not_called()
        self._assert_init_methods_called()

    def test_WorkbookElement_removeSheet_len_sheets_greater_1_parent_imp_not_equal(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet3'], autospec=True)
        _getImplementation = self._init_patch_with_name(
            '_getImplementation', 'xmind.core.Node.getImplementation',
            return_value='implementation', autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)
        _sheet = Mock()
        with patch.object(_sheet, 'getParentNode') as _getParentNode:
            _getParentNode.return_value = 'not equal'

            _result = _test_el.removeSheet(_sheet)

        _getSheets.assert_called_once_with(_test_el)
        _getParentNode.assert_called_once_with()
        _getImplementation.assert_called_once_with(_test_el)
        _removeChild.assert_not_called()
        _updateModifiedTime.assert_not_called()
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_removeSheet_len_sheets_greater_1_parent_imp_equal(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet3'], autospec=True)
        _getImplementation = self._init_patch_with_name(
            '_getImplementation', 'xmind.core.Node.getImplementation',
            return_value='implementation', autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)
        _sheet = Mock()
        with patch.object(_sheet, 'getParentNode') as _getParentNode:
            _getParentNode.return_value = 'implementation'

            _result = _test_el.removeSheet(_sheet)

        _getSheets.assert_called_once_with(_test_el)
        _getParentNode.assert_called_once_with()
        _getImplementation.assert_called_once_with(_test_el)
        _removeChild.assert_called_once_with(_test_el, _sheet)
        _updateModifiedTime.assert_called_once_with(_test_el)
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_removeSheet_sheets_is_none(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=None, autospec=True)

        with self.assertRaises(Exception) as _ex:
            _result = _test_el.removeSheet('sheet')

        _getSheets.assert_called_once_with(_test_el)
        self.assertTrue(_ex.exception.args[0].find(
            "object of type 'NoneType' has no len()") != -1)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_origin_index_less_then_0(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')

        with patch.object(_test_el, 'getSheets') as _getSheets:
            _getSheets.return_value = ['sheet1', 'sheet2', 'sheet3']

            _result = _test_el.moveSheet(-1, 1)

        _getSheets.assert_not_called()
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_origin_index_equal_target_index(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')

        with patch.object(_test_el, 'getSheets') as _getSheets:
            _getSheets.return_value = ['sheet1', 'sheet2', 'sheet3']

            _result = _test_el.moveSheet(2, 2)

        _getSheets.assert_not_called()
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_origin_index_not_less_0(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets', autospec=True)
        _getSheets.side_effect = Exception('test exception')

        with self.assertRaises(Exception) as _ex:
            _result = _test_el.moveSheet(0, 1)

        _getSheets.assert_called_once_with(_test_el)
        self.assertTrue(_ex.exception.args[0].find('test exception') == 0)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_origin_index_more_len_sheets(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')

        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)
        with patch.object(_test_el, 'getSheets') as _getSheets:
            _getSheets.return_value = ['sheet1', 'sheet2', 'sheet3']

            _result = _test_el.moveSheet(4, 1)

        _getSheets.assert_called_once_with()
        self.assertIsNone(_result)
        _updateModifiedTime.assert_not_called()
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_origin_index_equal_len_sheets(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')

        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)
        with patch.object(_test_el, 'getSheets') as _getSheets:
            _getSheets.return_value = ['sheet1', 'sheet2', 'sheet3']

            _result = _test_el.moveSheet(3, 1)

        _getSheets.assert_called_once_with()
        self.assertIsNone(_result)
        _updateModifiedTime.assert_not_called()
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_target_index_if_true(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')
        self._remove_patched_function('_appendChild')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet3'], autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result1 = _test_el.moveSheet(2, -1)
        self.assertIsNone(_result1)

        _result2 = _test_el.moveSheet(2, 4)
        self.assertIsNone(_result2)

        _result3 = _test_el.moveSheet(2, 5)
        self.assertIsNone(_result3)

        self.assertListEqual(_getSheets.call_args_list, [call(_test_el)]*3)
        self.assertListEqual(_removeChild.call_args_list, [
                             call(_test_el, 'sheet3')] * 3)
        self.assertListEqual(_appendChild.call_args_list, [
                             call(_test_el, 'sheet3')] * 3)
        self.assertListEqual(_updateModifiedTime.call_args_list, [
                             call(_test_el)] * 3)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_prev_true_origin_less_target_target_equal_sheet(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')
        self._remove_patched_function('_appendChild')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet_equal', 'sheet4', 'sheet_equal'], autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _insertBefore = self._init_patch_with_name(
            '_insertBefore', 'xmind.core.Node.insertBefore', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result = _test_el.moveSheet(2, 3)

        _getSheets.assert_called_once_with(_test_el)
        _removeChild.assert_not_called()
        _appendChild.assert_not_called()
        _insertBefore.assert_not_called()
        _updateModifiedTime.assert_called_once_with(_test_el)
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_prev_true_origin_greater_target_target_equal_sheet(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')
        self._remove_patched_function('_appendChild')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet_equal', 'sheet_equal', 'sheet5'], autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _insertBefore = self._init_patch_with_name(
            '_insertBefore', 'xmind.core.Node.insertBefore', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result = _test_el.moveSheet(3, 2)

        _getSheets.assert_called_once_with(_test_el)
        _removeChild.assert_not_called()
        _appendChild.assert_not_called()
        _insertBefore.assert_not_called()
        _updateModifiedTime.assert_called_once_with(_test_el)
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_prev_true_origin_greater_target_target_not_equal_sheet(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')
        self._remove_patched_function('_appendChild')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet_equal', 'sheet_not_equal', 'sheet5'], autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _insertBefore = self._init_patch_with_name(
            '_insertBefore', 'xmind.core.Node.insertBefore', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result = _test_el.moveSheet(3, 2)

        _getSheets.assert_called_once_with(_test_el)
        _removeChild.assert_called_once_with(_test_el, 'sheet_not_equal')
        _insertBefore.assert_called_once_with(
            _test_el, 'sheet_not_equal', 'sheet_equal')
        _appendChild.assert_not_called()
        _updateModifiedTime.assert_called_once_with(_test_el)
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_moveSheet_prev_true_origin_less_target_target_not_equal_sheet(self):
        _test_el = WorkbookElement()
        self._remove_patched_function('_getSheets')
        self._remove_patched_function('_updateModifiedTime')
        self._remove_patched_function('_appendChild')

        _getSheets = self._init_patch_with_name(
            '_getSheets', 'xmind.core.workbook.WorkbookElement.getSheets',
            return_value=['sheet1', 'sheet2', 'sheet_equal', 'sheet4', 'sheet_not_equal'], autospec=True)
        _removeChild = self._init_patch_with_name(
            '_removeChild', 'xmind.core.Node.removeChild', autospec=True)
        _appendChild = self._init_patch_with_name(
            '_appendChild', 'xmind.core.Node.appendChild', autospec=True)
        _insertBefore = self._init_patch_with_name(
            '_insertBefore', 'xmind.core.Node.insertBefore', autospec=True)
        _updateModifiedTime = self._init_patch_with_name(
            '_updateModifiedTime', 'xmind.core.mixin.WorkbookMixinElement.updateModifiedTime', autospec=True)

        _result = _test_el.moveSheet(2, 3)

        _getSheets.assert_called_once_with(_test_el)
        _removeChild.assert_called_once_with(_test_el, 'sheet_equal')
        _insertBefore.assert_called_once_with(
            _test_el, 'sheet_equal', 'sheet_not_equal')
        _appendChild.assert_not_called()
        _updateModifiedTime.assert_called_once_with(_test_el)
        self.assertIsNone(_result)
        self._assert_init_methods_called()

    def test_WorkbookElement_getVersion(self):
        _test_el = WorkbookElement()
        _getAttribute = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute',
            return_value='tested', autospec=True)

        _result = _test_el.getVersion()

        _getAttribute.assert_called_once_with(_test_el, ATTR_VERSION)
        self.assertEqual(_result, 'tested')
        self._assert_init_methods_called()
