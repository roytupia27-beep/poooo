#!/usr/bin/env python3
"""
=============================================================================
PUKLLAY SPORT - GESTIÓN Y AUDITORÍA DE USUARIOS CON CONTRASEÑA (PYTHON 3)
=============================================================================
Permite listar, crear, auditar y editar usuarios con verificación de
contraseñas hasheadas y en claro para el Administrador.
=============================================================================
"""

import sys
import json
from backend_poo import PukllayService, RolUsuario


def mostrar_ayuda():
    print("Uso:")
    print("  python3 gestionar_usuarios.py listar")
    print("  python3 gestionar_usuarios.py listar --json")
    print("  python3 gestionar_usuarios.py crear <nombre> <email> <telefono> <rol> [password]")
    print("  python3 gestionar_usuarios.py editar <user_id> <nombre> <email> <telefono> <rol> [password]")


def main():
    service = PukllayService()
    args = sys.argv[1:]

    if not args or args[0] in ["-h", "--help"]:
        mostrar_ayuda()
        return

    comando = args[0].lower()

    if comando == "listar":
        if "--json" in args:
            lista = [u.to_dict() for u in service.obtener_todos_usuarios()]
            print(json.dumps(lista, indent=2, ensure_ascii=False))
            return

        print("=" * 82)
        print(" 👥 PUKLLAY SPORT - DIRECTORIO DE USUARIOS Y CONTRASEÑAS (PYTHON)")
        print("=" * 82)
        print(f" {'ID':<12} | {'Nombre':<20} | {'Email':<24} | {'Teléfono':<11} | {'Rol':<14} | {'Contraseña'}")
        print("-" * 92)
        for u in service.obtener_todos_usuarios():
            print(f" {u.id:<12} | {u.nombre[:18]:<20} | {u.email[:22]:<24} | {u.telefono:<11} | {u.rol.value:<14} | {u.password_plano}")
        print("=" * 82)

    elif comando == "crear":
        if len(args) < 5:
            print("Error: Parámetros insuficientes. Ejemplo: python3 gestionar_usuarios.py crear 'Juan Perez' juan@gmail.com 991122334 CLIENTE Pukllay123*")
            return
        nombre = args[1]
        email = args[2]
        tel = args[3]
        rol_str = args[4].upper()
        passw = args[5] if len(args) > 5 else "Pukllay2026*"

        rol = getattr(RolUsuario, rol_str, RolUsuario.CLIENTE)
        nuevo = service.registrar_usuario(nombre, email, tel, rol, passw)
        print(f"✓ Usuario registrado con éxito: ID={nuevo.id}, Nombre='{nuevo.nombre}', Rol={nuevo.rol.value}, Password={nuevo.password_plano}")

    elif comando == "editar":
        if len(args) < 6:
            print("Error: Parámetros insuficientes. Ejemplo: python3 gestionar_usuarios.py editar cli_1 'Juan Carlos' juan@gmail.com 991122334 PROPIETARIO NuevaClave123*")
            return
        u_id = args[1]
        nombre = args[2]
        email = args[3]
        tel = args[4]
        rol_str = args[5].upper()
        passw = args[6] if len(args) > 6 else None

        rol = getattr(RolUsuario, rol_str, RolUsuario.CLIENTE)
        editado = service.actualizar_usuario(u_id, nombre, email, tel, rol, passw)
        print(f"✓ Usuario actualizado con éxito: ID={editado.id}, Nombre='{editado.nombre}', Rol={editado.rol.value}")

    else:
        print(f"Comando desconocido: '{comando}'")
        mostrar_ayuda()


if __name__ == "__main__":
    main()
