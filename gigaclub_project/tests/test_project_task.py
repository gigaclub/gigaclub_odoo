from odoo.tests import TransactionCase


class TestProjectTask(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_task = cls.env.ref("project.project_task_1")

    def test_get_all_tasks(self):
        self.assertTrue(self.project_task.get_all_tasks())

    def test_get_task(self):
        self.assertTrue(self.project_task.get_task(self.project_task.id))
        self.assertFalse(self.project_task.get_task(False))
