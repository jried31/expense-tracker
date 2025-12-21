import pytest
from unittest.mock import Mock, patch, call
from src.models.expense import Expense
from src.ui.menu import ExpenseTrackerMenu


@pytest.fixture
def mock_storage():
    """Create a mock storage instance."""
    return Mock()


@pytest.fixture
def menu(mock_storage):
    """Create ExpenseTrackerMenu instance with mock storage."""
    return ExpenseTrackerMenu(mock_storage)


class TestExpenseTrackerMenu:
    def test_menu_initialization(self, mock_storage):
        """Test menu creation."""
        menu = ExpenseTrackerMenu(mock_storage)
        assert menu.storage == mock_storage

    def test_display_menu(self, menu):
        """Verify menu renders correctly."""
        with patch('builtins.print') as mock_print:
            with patch.object(menu, 'clear_screen'):
                menu.display_menu()

                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)

                assert 'EXPENSE TRACKER' in output
                assert '1. Add New Expense' in output
                assert '2. List All Expenses' in output
                assert '3. View Expenses by Category' in output
                assert '4. Delete Expense' in output
                assert '5. Exit' in output

    def test_get_user_choice(self, menu):
        """Test getting user choice."""
        with patch('builtins.input', return_value='2'):
            choice = menu.get_user_choice()
            assert choice == '2'

    def test_list_expenses_empty(self, menu, mock_storage):
        """Test listing with no expenses."""
        mock_storage.load_all_expenses.return_value = []

        with patch('builtins.print') as mock_print:
            menu.list_expenses()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ''.join(calls)
            assert 'No expenses found' in output

    def test_list_expenses_with_data(self, menu, mock_storage):
        """Test listing with expenses."""
        expense1 = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        expense2 = Expense(30, "Transport", "Taxi", expense_id="exp_2", created_at="2025-12-21T13:00:00")
        mock_storage.load_all_expenses.return_value = [expense1, expense2]

        with patch('builtins.print') as mock_print:
            menu.list_expenses()

            mock_storage.load_all_expenses.assert_called_once()

            all_calls = [call[0][0] if call[0] else '' for call in mock_print.call_args_list]
            output = ' '.join([str(item) for item in all_calls])

            assert 'TOTAL' in output
            assert '80' in output or '80.00' in output
            assert mock_print.call_count >= 5

    def test_add_expense_flow(self, menu, mock_storage):
        """Mock user input and verify expense saved."""
        with patch('src.ui.menu.get_valid_input') as mock_input:
            with patch('builtins.input', side_effect=['Test lunch', '']):
                mock_input.side_effect = [50.99, 'Food', '2025-12-21']

                with patch('builtins.print'):
                    menu.add_expense()

                mock_storage.save_expense.assert_called_once()
                saved_expense = mock_storage.save_expense.call_args[0][0]
                assert saved_expense.amount == 50.99
                assert saved_expense.category == 'Food'

    def test_add_expense_with_validation_error(self, menu, mock_storage):
        """Test add expense with validation error."""
        with patch('src.ui.menu.get_valid_input', side_effect=ValueError("Invalid amount")):
            with patch('builtins.print') as mock_print:
                menu.add_expense()

                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'Error' in output or 'Invalid' in output

    def test_view_expenses_by_category(self, menu, mock_storage):
        """Test viewing expenses grouped by category."""
        expense1 = Expense(50, "Food", "Lunch", expense_id="exp_1")
        expense2 = Expense(30, "Food", "Dinner", expense_id="exp_2")
        expense3 = Expense(20, "Transport", "Taxi", expense_id="exp_3")
        mock_storage.load_all_expenses.return_value = [expense1, expense2, expense3]

        with patch('builtins.print') as mock_print:
            menu.view_expenses_by_category()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ''.join(calls)

            assert 'Food' in output
            assert 'Transport' in output
            assert 'Subtotal' in output
            assert 'GRAND TOTAL' in output

    def test_delete_expense_success(self, menu, mock_storage):
        """Test successful expense deletion."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        mock_storage.load_all_expenses.return_value = [expense]
        mock_storage.delete_expense.return_value = True

        with patch('builtins.input', side_effect=['1', 'y']):
            with patch('builtins.print') as mock_print:
                menu.delete_expense()

                mock_storage.delete_expense.assert_called_once_with('exp_1')
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'deleted successfully' in output or 'Expense deleted' in output

    def test_delete_expense_cancelled(self, menu, mock_storage):
        """Test cancelled deletion with 'n' response."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        mock_storage.load_all_expenses.return_value = [expense]

        with patch('builtins.input', side_effect=['1', 'n']):
            with patch('builtins.print') as mock_print:
                menu.delete_expense()

                mock_storage.delete_expense.assert_not_called()
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'cancelled' in output

    def test_delete_expense_cancelled_empty_input(self, menu, mock_storage):
        """Test cancelled deletion by pressing Enter."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        mock_storage.load_all_expenses.return_value = [expense]

        with patch('builtins.input', return_value=''):
            with patch('builtins.print') as mock_print:
                menu.delete_expense()

                mock_storage.delete_expense.assert_not_called()
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'cancelled' in output

    def test_delete_expense_empty_list(self, menu, mock_storage):
        """Test delete when no expenses exist."""
        mock_storage.load_all_expenses.return_value = []

        with patch('builtins.print') as mock_print:
            menu.delete_expense()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ''.join(calls)
            assert 'No expenses found' in output

    def test_run_exit(self, menu):
        """Test exiting the menu."""
        with patch.object(menu, 'display_menu'):
            with patch.object(menu, 'get_user_choice', return_value='5'):
                with patch('builtins.print') as mock_print:
                    menu.run()

                    calls = [str(call) for call in mock_print.call_args_list]
                    output = ''.join(calls)
                    assert 'Goodbye' in output or 'Thank you' in output

    def test_run_menu_loop(self, menu, mock_storage):
        """Test menu loop with multiple choices."""
        mock_storage.load_all_expenses.return_value = []

        with patch.object(menu, 'display_menu'):
            with patch.object(menu, 'get_user_choice', side_effect=['2', '5']):
                with patch('builtins.input', return_value=''):
                    with patch('builtins.print'):
                        menu.run()

                        assert mock_storage.load_all_expenses.called

    def test_clear_screen(self, menu):
        """Test clear screen functionality."""
        with patch('os.system') as mock_system:
            menu.clear_screen()
            mock_system.assert_called_once()

    def test_run_with_add_expense(self, menu, mock_storage):
        """Test menu loop with add expense choice."""
        with patch.object(menu, 'display_menu'):
            with patch.object(menu, 'get_user_choice', side_effect=['1', '5']):
                with patch.object(menu, 'add_expense') as mock_add:
                    with patch('builtins.input', return_value=''):
                        with patch('builtins.print'):
                            menu.run()
                            mock_add.assert_called_once()

    def test_run_with_view_by_category(self, menu, mock_storage):
        """Test menu loop with view by category choice."""
        mock_storage.load_all_expenses.return_value = []
        with patch.object(menu, 'display_menu'):
            with patch.object(menu, 'get_user_choice', side_effect=['3', '5']):
                with patch('builtins.input', return_value=''):
                    with patch('builtins.print'):
                        menu.run()
                        mock_storage.load_all_expenses.assert_called()

    def test_run_with_delete_expense(self, menu, mock_storage):
        """Test menu loop with delete expense choice."""
        mock_storage.load_all_expenses.return_value = []
        with patch.object(menu, 'display_menu'):
            with patch.object(menu, 'get_user_choice', side_effect=['4', '5']):
                with patch('builtins.input', return_value=''):
                    with patch('builtins.print'):
                        menu.run()
                        mock_storage.load_all_expenses.assert_called()

    def test_run_with_invalid_choice(self, menu):
        """Test menu with invalid choice."""
        with patch.object(menu, 'display_menu'):
            with patch.object(menu, 'get_user_choice', side_effect=['99', '5']):
                with patch('builtins.print') as mock_print:
                    menu.run()
                    calls = [str(call) for call in mock_print.call_args_list]
                    output = ''.join(calls)
                    assert 'Invalid' in output or 'invalid' in output

    def test_add_expense_keyboard_interrupt(self, menu):
        """Test add expense with keyboard interrupt."""
        with patch('src.ui.menu.get_valid_input', side_effect=KeyboardInterrupt()):
            with patch('builtins.print') as mock_print:
                menu.add_expense()
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'cancelled' in output or 'Operation cancelled' in output

    def test_delete_expense_invalid_number(self, menu, mock_storage):
        """Test delete with invalid number input."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        mock_storage.load_all_expenses.return_value = [expense]

        with patch('builtins.input', return_value='abc'):
            with patch('builtins.print') as mock_print:
                menu.delete_expense()
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'Invalid' in output or 'invalid' in output

    def test_delete_expense_out_of_range(self, menu, mock_storage):
        """Test delete with out of range number."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        mock_storage.load_all_expenses.return_value = [expense]

        with patch('builtins.input', side_effect=['99', '']):
            with patch('builtins.print') as mock_print:
                menu.delete_expense()
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'Invalid' in output or 'invalid' in output

    def test_delete_expense_keyboard_interrupt(self, menu, mock_storage):
        """Test delete with keyboard interrupt."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_1", created_at="2025-12-21T12:00:00")
        mock_storage.load_all_expenses.return_value = [expense]

        with patch('builtins.input', side_effect=KeyboardInterrupt()):
            with patch('builtins.print') as mock_print:
                menu.delete_expense()
                calls = [str(call) for call in mock_print.call_args_list]
                output = ''.join(calls)
                assert 'cancelled' in output or 'Operation cancelled' in output
