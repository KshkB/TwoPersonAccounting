# Accounts for two

## Outline of repository 

This repository contains the Python program `BillSplitterForTwo` which, once run, prompts to the user to:

- create a new file;
- add a transaction (to an existing file);
- show account balances;
- quit.

The program creates or updates an `.xlsx` file in the same folder containing the program itself.

## The accounting system

This program is tailored to accounting for *two* people. Not three or higher. The `.xlsx` file created contains two sheets, one for each person.
On each person's sheet the following fields are created:

- description;
- total amount;
- taxes;
- additional costs;
- person's amount;
- amount paid by person;
- what they are owed/owed;
- external debts.

Upon creating a file, the above fields are initialised. When adding a transaction, the user is prompted to fill in each field.

The program itself passes no values and relies on user inputs.

## Mechanics of the system

### Foundations

As mentioned, this system is tailored to record-keeping for two people, say person $A$ and person $B$. In a given transaction there are a few parameters to account for: the amounts actually paid by each person $A$ and $B$, say $x_A$ and $x_B$ respectively. The amounts in the transaction that each person actually owes, say $y_A$ and $y_B$. And finally the total value of the transaction itself, say $t$. 

By construction $t = y_A + y_B$. The value of the transaction is made up of what each person in the transaction *actually* owes. This must be reconciled with what each person actually paid. 

There are three scenarios to now consider: where the totals paid equals the total, is overpaid or underpaid. That is:

- $x_A + x_B = t$;
- $x_A + x_B > t$;
- $x_A + x_B < t$.

#### When equal

Recall, it is always the case that $y_A + y_B = t$. With $x_A + x_B = t$ also, what matters is the relative differences $x_A - y_A$ and $x_B - y_B$. If these differences are zero, then person $A$ and $B$ paid what they owe and there is no issue. No one owes the other. In the case where, say, $x_A - y_A > 0$, this means $A$ paid what they owe *and* part of person $B$ owes. Hence that $B$ underpaid, The accounting system records $x_A - y_A$ in $A$'s column `owed/owes`. In $B$'s column, the system records $x_B - y_B$. This is the amount $B$ owes $A$.

**Note.** In this case $x_A - y_A = -(x_B - y_B)$, so the debts recorded as above are indeed balanced. To see why this equality holds, note that upon rearranging we find $x_A + x_B = y_A + y_B = t$, which is what we assumed at the outset.

#### Overpaid

In this case $x_A + x_B > t$, so each person has in combination *overpaid* what they owe. They are therefore entitled to change $c = (x_A + x_B) - t$. In the accounting system this change is redistributed back to each person in proportion to what they paid. That is, person $A$ receives change $c_A = \frac{x_A}{x_A + x_B}c$ and person $B$ receives $c_B = \frac{x_B}{x_A + x_B}c$. 

Upon redistribution, each person's *effective pay* is: $\tilde x_A = x_A - c_A$ and $\tilde x_B = x_B - c_B$. Note that now $\tilde x_A + \tilde x_B = t$ and we are in the situation above where the combined payment is equal to the total owed, $t$. The system above can then be used to record this transaction and any debt owed.


#### Underpaid

This scenario is more difficult to account for since, in this case, $x_A + x_B < t$ entailing a new debt obligation. On each person's sheet in the spreadsheet one finds a record in the `external debts` column. 

Now if both persons underpay, $x_A < y_A$ and $x_B < y_B$. Hence each owes the external debtor an amount $|x_A - y_A|$ and $|x_B - y_B|$ respectively. The accounting system records the raw value $x_A - y_A$ and $x_B - y_B$ in the `external debts` column on the respective spreadsheets.

In the case where one of the persons pay what they owe while the other fails, e.g., $x_A = y_A$ but $x_B < y_B$, then there is a debt obligation $x_B - y_B$. This is born entirely by person $B$. Accordingly person $A$ does not record any external debt and $B$ records an external debt of $x_B - y_B$. Note that $B$ does not owe $A$ anything.

Finally, we have the subtle case where one overpays and the other underpays to the point of total underpayment. So e.g., $x_A > y_A$ and $x_B < y_B$ and $x_A + x_B < t$. In this case $A$ has paid what they owe and some of what $B$ owes; $B$ now owes both an external debt and a debt to $A$. The *external debt* which $B$ owes is what remains on the bill, $(x_A + x_B) - t$. 

The debt owed by $B$ to $A$ is $x_A - y_A$, the excess which $A$ paid over what they owed.

**Note.** Recording the debt owed by $B$ in this way is indeed consistent. That is, the total debt owed by $B$ is what they paid less what they owe, i.e., $x_B - y_B$. That is each of $B$'s debts, $(x_A + x_B) - t$ and $-(x_A - y_A)$, will sum to precisely what remains on what $B$ owes. That is $((x_A + x_B) - t) + (-(x_A - y_A)) = x_B - y_B$.

## Example transactions

### When equal

Suppose Alice and Balkrishna split a taxi fare. The taxi costs $500$ in whatever currency. As they are splitting the fare, each owes $250$. Accordingly $y_A = 250$ and $y_B = 250$. When they pay suppose that:

- Alice pays $350$; Balkrishna pays $150$. 

Then $x_A = 350$ and $x_B = 150$. Note that $x_A + x_B = 500$ so there is no change or external debt. The accounting system will record $x_A - y_A = 350 - 250 = 100$ in Alice's `owed/owes` column. It will likewise record $x_B - y_B = 150 - 250 = -100$ in Balkrishna's `owed/owes` column. 

Balkrishna owes Alice $100$. 

### Overpaid

Alice and Balkrishna took that taxi to a restaurant for dinner. Alice had the sirloin pork cutlet and Balkrishna a full spit roast. Suppose the dinner for both cost 1500. Of this:

- Alice paid $600$ while Balkrishna pids $1200$. 

Then $x_A + x_B = 600 + 1200 = 1800$. This exceeds the amount owed for dinner, being $1500$, resulting in change $1800 - 1500 = 300$. Of the total amount paid, $1800$, Alice paid $1/3$; Balkrishna $2/3$. Hence Alice gets back $(1/3)(300) = 100$ in change; Balkrishna $(2/3)(300) = 200$ in change. Their respective *effective* payments are $\tilde x_A = 600 - 100 = 500$ and $\tilde x_B = 1200 - 200 = 1000$. Note $\tilde x_A + \tilde x_B = 1500$. 

Suppose now that the cost of Alice's dish is $y_A = 700$; and Balkrishna's is $y_B = 800$. The accounting system will record $x_A - y_A = 500 - 700 = -200$ in Alice's `owed/owes` column; and in Balkrishna's `owed/owes` column $x_B - y_B = 1000 - 800 = 200$. 

Combined with the taxi fare, Alice's `owed/owes` column is $100 + (-200) = -100$ and Balkrishna's `owed/owes` column is $-100 + 200 = 100$. Hence Alice now owes Balkrishna an amount of $100$.

### Underpaid

Alice and Balkrishna are running out of cash. On the taxi ride back from the restaurant to wherever they came from, suppose the fare is $500$ and:

- Alice pays $x_A = 350$; Balkrishna pays $x_B = 100$.

The total amount paid is $x_A + x_B = 350 + 100 = 450$, which is $50$ short of what is owed. This thereby creates an external debt obligation. Am amount of $50$ needs to be paid to the taxi driver. 

Alice owed $y_A = 250$ and Balkrishna $y_B = 250$. Since $x_A = 350 > 250$, Alice does not record an external debt. Balkrishna however *does* record such a debt, in an amount of $(x_A + x_B) - t = (350 + 100) - 500 = -50$. Moreover, since Alice overpaid what was owed, $x_A - y_A = 350 - 250 = 100$, Alice's `owed/owes` column records $+100$. On Balkrishna's records, an amount $x_B - y_B + c = 100 - 250 + 50 = -100$ is recorded. This transaction brings Balkrishna back into debt toward Alice. 

Now in combination with the other two transactions, see that Alice's `owed/owes` column is $-100 + (+ 100) = 0$ and Balkrishna's column is $100 + (-100) = 0$. Hence Alice and Balkrishna are in fact all settled up. It remains for Balkrishna to pay the taxi driver $50$, as recorded in Balkrishna's `external debts` column.

**Remark.** As an exercise in using this accounting system, record the above three transactions.


