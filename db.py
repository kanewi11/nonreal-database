class Database:
    NOT_FOUND = 'NULL'

    def __init__(self):
        self.__data = {}
        self.__transactions = []
        self.__connection = True

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
                    return transaction[key] or self.NOT_FOUND
        return self.__data.get(key, self.NOT_FOUND)

    def unset(self, key):
        if self.__transactions:
            current_transaction = self.__transactions[-1]
            current_transaction[key] = None
        else:
            self.__data.pop(key, None)

    def counts(self, value):
        count = 0
        found_keys = set()

        if self.__transactions:
            for transaction in reversed(self.__transactions):
                for key, transaction_value in transaction.items():
                    if transaction_value is None:
                        found_keys.add(key)
                    elif key not in found_keys and transaction_value == value:
                        count += 1
                        found_keys.add(key)

        for key, data_value in self.__data.items():
            if key not in found_keys and data_value == value:
                count += 1
        return count

    def find(self, value):
        found = set()
        unset_keys = set()
        if self.__transactions:
            for transaction in reversed(self.__transactions):
                for key, transaction_value in transaction.items():
                    if transaction_value is None:
                        unset_keys.add(key)
                    elif transaction_value == value:
                        found.add(key)

        for key, data_value in self.__data.items():
            if data_value == value and key not in unset_keys:
                found.add(key)
        return list(found)

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

        for key, value in self.__data.items():
            if value is None:
                self.__data.pop(key, None)

    def end(self):
        self.__connection = False

    def connection(self):
        return self.__connection

    def query(self, query_):
        if not query_:
            return
        elif query_ == 'END':
            self.end()
            return

        tokens = query_.split()
        command = tokens[0]

        if command == 'SET' and len(tokens) == 3:
            key, value = tokens[1], tokens[2]
            self.set(key, value)
        elif command == 'BEGIN':
            self.begin()
        elif command == 'ROLLBACK':
            self.rollback()
        elif command == 'COMMIT':
            self.commit()
        elif len(tokens) != 2:
            return 'Missing an argument'
        elif command == 'GET':
            key = tokens[1]
            return self.get(key)
        elif command == 'UNSET':
            key = tokens[1]
            self.unset(key)
        elif command == 'COUNTS':
            value = tokens[1]
            return self.counts(value)
        elif command == 'FIND':
            value = tokens[1]
            return ' | '.join(self.find(value))
        else:
            return 'Incorrect query: ' + query_


def main():
    db = Database()

    while True:
        query = raw_input().strip()
        data = db.query(query)
        if not db.connection():
            break
        if data is not None:
            print data


if __name__ == '__main__':
    try:
        main()
    except EOFError:
        print 'Exiting...'
    except Exception as error:
        print str(error)
        raw_input('Press Enter to exit...')
