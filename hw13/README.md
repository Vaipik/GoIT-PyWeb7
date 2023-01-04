<h3>Finance helper</h3>

This project has been created to help you with your finance controlling.
          As user of this finance helper, helper in further, you are able to do following things:
<ul>
          <li>Create, edit or delete different accounts according to your wishes</li>
              All your created accounts will be shown on the right side of each page. Even if account is empty.
              To open desired account just click on it.
          <li>Add, edit, delete transactions in each account.
            <ul>
              <li>
                When you are adding new transaction you can specify a category, if you leave the category field empty
                it will be <u>automatically</u> set to <i>No category</i>.
              </li>
              <li>
                You are not able to set date when adding new transaction. It will be set automatically.
              </li>
              <li>
                When you are editing a transaction data you can also can change the date.
                  Note that you must enter date in the same format as it will be shown.
              </li>
                <li>
                If you have already added a transaction with or without category it will be shown on the left side of each page.
                  You are able to click on category name and all your transactions with this category divided by accounts will be shown.
                </li>
            </ul>
          </li>
          <li>
            On the main page all your accounts are presented. They are shown by using pagination. On each page presented
            <u>maximum 3 accounts</u> with <u>maximum 5 last transactions</u>.
            Accounts ordering are similar to transactions ordering. Ordering by date descending.
            If you want to see more transactions in an account just click on its name.
          </li>
          <li>
            On an account page you can see all transactions related to this account.
            On each page will be shown maximum 7 transactions.
            Default ordering is date descending, but you are able to order them in different ways: description, amount,
            category, remaining balance or again date.
            <br>Note that transactions will be ordered also in descending way.
          </li>
          <li>
            On the top right corner search field is presented.
            You can search transactions by amount or description match, but you cannot search for category.
            You are able to enter into the field words, letters, digits as much as you want and in different order.
            <br>
            The result will be presented similar to main page. ALl matched transactions will be divided into accounts.
          </li>
</ul>
Project contains from two applications:
<ol>
    <li>finances - main application with all mentioned below functionallity</li>
    <li>users - application for registration and authentification users.</li>
    It means that each user can handle <b>ONLY</b> with his data.
</ol>

Requirements to this project:
* python = ^3.10
* django = ^4.1.4
* django-autoslug = ^1.9.8  -> autoslug field for django orm 
* psycopg2 = ^2.9.5  -> connector to postgresql db
* pytils = ^0.4.1  -> to proper django-autoslug work with cyrillic symbols.
