from bank.models import Account, User

class AccountUtils:
    
    @staticmethod
    def create_new_account(user: User ) -> int:
        number_account = Account.objects.count() + 1
        account = Account(agency=1, account=number_account, user=user, saldo=0.00, )
        pk_account = account.save()
        return  pk_account 