import sqlite3

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class AuthenticationSystem:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.current_user = None

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")

    def create_user(self, username, password, role):
        user = User(username, password, role)
        self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user.username, user.password, user.role))
        self.conn.commit()
        print("L'utilisateur {} a été créé avec succès.".format(username))

    def login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = self.cursor.fetchone()
        if user_data:
            self.current_user = User(user_data[0], user_data[1], user_data[2])
            print("Connexion réussie. Bonjour, {}!".format(self.current_user.username))
        else:
            print("Échec de la connexion. Veuillez vérifier votre nom d'utilisateur et votre mot de passe.")

    def logout(self):
        if self.current_user is not None:
            print("Déconnexion réussie. Au revoir, {}!".format(self.current_user.username))
            self.current_user = None
        else:
            print("Aucun utilisateur connecté.")

    def get_user_credentials(self, admin_username):
        if self.current_user is not None and self.current_user.role == "admin" and self.current_user.username == admin_username:
            self.cursor.execute("SELECT username, password FROM users")
            user_credentials = self.cursor.fetchall()
            for credential in user_credentials:
                print("Nom d'utilisateur : {}, Mot de passe : {}".format(credential[0], credential[1]))
        else:
            print("Action non autorisée.")

    def delete_user(self, admin_username, username):
        if self.current_user is not None and self.current_user.role == "admin" and self.current_user.username == admin_username:
            self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            self.conn.commit()
            print("L'utilisateur {} a été supprimé avec succès.".format(username))
        else:
            print("Action non autorisée.")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

# Fonction principale
def main():
    auth_system = AuthenticationSystem()

    while True:
        print("\n=== Système d'authentification ===")
        print("1. Créer un utilisateur")
        print("2. Se connecter")
        print("3. Se déconnecter")
        print("4. Afficher les identifiants des utilisateurs (réservé à l'admin)")
        print("5. Supprimer un utilisateur (réservé à l'admin)")
        print("6. Quitter")

        choice = input("Veuillez sélectionner une option : ")

        if choice == "1":
            username = input("Nom d'utilisateur : ")
            password = input("Mot de passe : ")
            role = input("Rôle (admin/finance/user) : ")
            auth_system.create_user(username, password, role)

        elif choice == "2":
            username = input("Nom d'utilisateur : ")
            password = input("Mot de passe : ")
            auth_system.login(username, password)

        elif choice == "3":
            auth_system.logout()

        elif choice == "4":
            admin_username = input("Nom d'utilisateur admin : ")
            auth_system.get_user_credentials(admin_username)

        elif choice == "5":
            admin_username = input("Nom d'utilisateur admin : ")
            username = input("Nom d'utilisateur à supprimer : ")
            auth_system.delete_user(admin_username, username)

        elif choice == "6":
            break

        else:
            print("Option invalide. Veuillez sélectionner une option valide.")

if __name__ == "__main__":
    main()



