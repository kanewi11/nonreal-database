class Database:
    NOT_FOUND = 'NULL'

    __data = {}

    def __init__(self):
        self.__transactions = []

    def set(self, key, value):
        if self.__transactions:
            current_transaction = self.__transactions[-1]
            current_transaction[key] = value
        else:
            self.__data[key] = value

    def get(self, key):
        if self.__transactions:
            for transaction in reversed(self.__transactions):
                if key in transaction:
                    return transaction[key]
        return self.__data.get(key, self.NOT_FOUND)

    def unset(self, key):
        if self.__transactions:
            current_transaction = self.__transactions[-1]
            current_transaction.pop(key, None)
        else:
            self.__data.pop(key, None)

    def counts(self, value):
        count = 0
        if self.__transactions:
            for transaction in reversed(self.__transactions):
                count += list(transaction.values()).count(value)
        else:
            count += list(self.__data.values()).count(value)
        return count

    def find(self, value):
        found = []
        if self.__transactions:
            for transaction in reversed(self.__transactions):
                found += [key for key, val in transaction.items() if val == value]
        else:
            found += [key for key, val in self.__data.items() if val == value]
        return found

    def begin(self):
        self.__transactions.append({})

    def rollback(self):
        if self.__transactions:
            self.__transactions.pop()

    def commit(self):
        if self.__transactions:
            for transaction in self.__transactions:
                self.__data.update(transaction)
            self.__transactions = []


def main():
    db = Database()

    while True:
        command = input().strip()
        if not command:
            continue
        if command == 'END':
            break

        tokens = command.split()
        cmd = tokens[0]

        if cmd == 'SET' and len(tokens) == 3:
            key, value = tokens[1], tokens[2]
            db.set(key, value)
        elif cmd == 'GET':
            key = tokens[1]
            print(db.get(key))
        elif cmd == 'UNSET':
            key = tokens[1]
            db.unset(key)
        elif cmd == 'COUNTS':
            value = tokens[1]
            print(db.counts(value))
        elif cmd == 'FIND':
            value = tokens[1]
            print(' | '.join(db.find(value)))
        elif cmd == 'BEGIN':
            db.begin()
        elif cmd == 'ROLLBACK':
            db.rollback()
        elif cmd == 'COMMIT':
            db.commit()
        else:
            print('Некорректная команда:', cmd)


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        pass
