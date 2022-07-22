import os, sys
import pandas as pd

def billSplit():
    print("Choose:\n1. Create new file\n2. Add transaction\n3. Show balances\n4. Whoops, ran this by accident. I'm a celebrity, get me outta here!")
    ans = int(input().strip())

    if ans == 1:
        print('Enter the file name:')
        file_name = str(input().strip())
        file_name = file_name + '.xlsx'
        print("Enter the first person's name:")
        name_1 = str(input().strip())

        print("Enter the second person's name:")
        name_2 = str(input().strip())

        name1_columns = [
            'Description',
            'Total amount due',
            'Taxes',
            'Additional costs',
            f"{name_1}'s amount",
            f"{name_1} paid", 
            "Owed/owes (+/-)",
            "External debts"
        ]

        name2_columns = [
            'Description',
            'Total amount due',
            'Taxes',
            'Additional costs',
            f"{name_2}'s amount",
            f"{name_2} paid",
            "Owed/owes (+/-)",
            "External debts"
        ]

        dataframe_1 = pd.DataFrame(columns = name1_columns)
        dataframe_1 = dataframe_1.append(
            pd.Series(
                [
                    'initialized', 0, 0, 0, 0, 0, 0, 0
                ], index=name1_columns
            ), ignore_index=True
        )

        dataframe_2 = pd.DataFrame(columns = name2_columns)
        dataframe_2 = dataframe_2.append(
            pd.Series(
                [ 
                  'initialized', 0, 0, 0, 0, 0, 0, 0  
                ], index=name2_columns
            ), ignore_index=True
        )

        sprdsheet = pd.ExcelWriter(file_name, engine='xlsxwriter')

        dataframe_1.to_excel(sprdsheet, sheet_name = name_1, index=False)
        dataframe_2.to_excel(sprdsheet, sheet_name= name_2, index=False)

        sprdsheet.save()

        os.system('clear')
        print('Keep going? (Y/N)')
        response = str(input().strip())
        if response == 'Y':
            return billSplit()
        else:
            sys.exit(0)

    if ans == 2:
        print('Enter the file name:')
        file_name = str(input().strip())
        file_name = file_name + '.xlsx'
        if bool(os.path.isfile(file_name)):
            os.system('clear')
            print('Cool, it is here!')

            xl_data = pd.ExcelFile(file_name)
            
            description = {}
            print('Description of the transaction:')
            description['Description'] = str(input().strip())

            numerical_inputs = {
                'Total amount due':'',
                'Taxes':'',
                'Additional costs':''
            }

            for item in numerical_inputs:
                print(f'Enter a value for {item}:')
                val = float(input().strip())
                numerical_inputs[item] = val

            payment_record = {}
            for name in xl_data.sheet_names:
                payment_record[f"{name}"] = {}
                payment_record[f"{name}"][f"{name}'s amount"] = ''
                payment_record[f"{name}"][f"{name} paid"] = ''                

            for name in xl_data.sheet_names:
                for item in payment_record[f"{name}"]:
                    print(f"Enter the value for {item}")
                    val = float(input().strip())
                    payment_record[f'{name}'][item] = val

            for name in xl_data.sheet_names:
                prev_outstanding = xl_data.parse(name).iloc[-1]['Owed/owes (+/-)']
                payment_record[f"{name}"]["Owed/owes (+/-)"] = prev_outstanding

            #    prev_still_owed = xl_data.parse(name).iloc[-1]["External debts"]
                payment_record[f"{name}"]["External debts"] = 0


            sprdsheet = pd.ExcelWriter(file_name, engine='xlsxwriter')

            
            total = numerical_inputs['Total amount due']
            tax = 1 + numerical_inputs['Taxes']
            additional = numerical_inputs['Additional costs']
            total = total*tax + additional

            total_paid = sum(
                [
                    payment_record[f"{name}"][f"{name} paid"] for name in xl_data.sheet_names
                ]
            )
            change = total_paid - total
            
            if change > 0:
                for name in xl_data.sheet_names:
                    proportion = payment_record[f"{name}"][f"{name} paid"]/total_paid 
                    payment_record[f"{name}"][f"{name} paid"] += -proportion*change

            if change < 0:
                for name in xl_data.sheet_names:
                    paid = payment_record[f"{name}"][f"{name} paid"]
                    owed = payment_record[f"{name}"][f"{name}'s amount"]
                    owed = owed*tax + (owed/total)*additional

                    if paid >= owed:
                        payment_record[f"{name}"]["External debts"] = 0
                    else:
                        if - (paid - owed) + change < 0:
                            #payment_record[f"{name}"][f"{name}'s amount"] = 0
                            #payment_record[f"{name}"][f"{name} paid"] = 0
                            payment_record[f"{name}"]["External debts"] = paid - owed
                        if - (paid - owed) + change > 0:
                            payment_record[f"{name}"]["External debts"] = change 
                            #payment_record[f"{name}"][f"{name} paid"] = owed - (- (paid - owed) + change)
                            

            transactions = {}
            for name in xl_data.sheet_names:
                owed = payment_record[f"{name}"][f"{name}'s amount"]
                owed = owed*tax + (owed/total)*additional
                paid = payment_record[f"{name}"][f"{name} paid"]
                extdebt = payment_record[f"{name}"]["External debts"]

                payment_record[f"{name}"]['Owed/owes (+/-)'] += paid - owed - extdebt

                transactions[f"{name}"] = {**description, **numerical_inputs, **payment_record[f"{name}"]}

                xl_df = xl_data.parse(name)
                xl_df = xl_df.append(
                    pd.Series(
                        [
                        transactions[f"{name}"][item] for item in transactions[f"{name}"]
                        ], index = xl_df.columns
                    ), ignore_index=True
                )

                xl_df.to_excel(sprdsheet, sheet_name = name, index=False)

            sprdsheet.save()

            os.system('clear')
            print('Keep going? (Y/N)')
            response = str(input().strip())
            if response == 'Y':
                return billSplit()
            else:
                sys.exit(0)

        else:
            os.system('clear')
            print('Not here mate. Try again.')
            billSplit()

    if ans == 3:
        print('Enter the name of the file you want to check:')
        file_name = str(input().strip())
        file_name = file_name + '.xlsx'
        if bool(os.path.isfile(file_name)):
            os.system('clear')
            print('Cool, it is here!')

            xl_data = pd.ExcelFile(file_name)
            print('Whose balance do you want to see:')
            num_name = {}
            for i, name in enumerate(xl_data.sheet_names):
                num_name[i] = name
                print(f"{i}. {name}")
            print('3. See all')
            usr_ans = int(input().strip())
            
            os.system('clear')
            if usr_ans <=2:
                df = xl_data.parse(num_name[usr_ans])
                print(df.to_string(index=False))

            if usr_ans == 3:
                for name in xl_data.sheet_names:
                    df = xl_data.parse(name)
                    print(f"{name}'s records:")
                    print(df.to_string(index=False))
                    print('\n')

            

            print('\nKeep going? (Y/N)')
            response = str(input().strip())
            if response == 'Y':
                os.system('clear')
                return billSplit()
            else:
                sys.exit(0)

        else:
            os.system('clear')
            print('Not here mate. Try again.\n')
            billSplit()

    if ans == 4:
        sys.exit(0)

if __name__ == '__main__':
    os.system('clear')
    billSplit()

