import re
import json
from graphviz import Digraph
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
from automata.base.exceptions import RejectionException


class AutomataProject:
    def __init__(self):
        self.afn = None
        self.afd = None

    def ingresar_expresion_regular(self):

        expr = input("Ingrese la expresión regular: ")
        return expr

    def generar_afn(self, expr):
        # Simplificación: en lugar de convertir manualmente la expresión regular,
        # usamos automata-lib para crear el AFN
        self.afn = NFA.from_regex(expr)
        print(f"AFN generado: {self.afn}")

    def convertir_a_afd(self):
        self.afd = DFA.from_nfa(self.afn)
        print(f"AFD generado: {self.afd}")
        self.guardar_afd()

    def guardar_afd(self):
        afd_dict = {
            "states": list(self.afd.states),
            "input_symbols": list(self.afd.input_symbols),
            "transitions": self.afd.transitions,
            "initial_state": self.afd.initial_state,
            "final_states": list(self.afd.final_states)
        }
        with open('AFD.txt', 'w') as file:
            json.dump(afd_dict, file, indent=4)
        print("AFD guardado en AFD.txt")

    def validar_cadena(self, cadena):
        try:
            if self.afd.accepts_input(cadena):
                print(f"La cadena '{cadena}' es aceptada por el AFD.")
            else:
                print(f"La cadena '{cadena}' no es aceptada por el AFD.")
        except RejectionException:
            print(f"La cadena '{cadena}' no es aceptada por el AFD.")

    # Funcion para generar una imagen de la automata convertida AFD
    # a partir de una expresion regular
    def generar_diagrama(self, dfa, tittle):
        dot = Digraph()

        if tittle:
            dot.attr(label= tittle, labelloc='t', fontsize='20')

        # Definir los estados finales
        for state in dfa.states:
            if state in dfa.final_states:
                dot.node(str(state), shape='doublecircle')
            else:
                dot.node(str(state))
        # Definir los estados de la automata
        for state, transitions in dfa.transitions.items():
            for symbol, next_state in transitions.items():
                dot.edge(str(state), str(next_state), label=symbol)

        return dot

    def generar_diagrama_afn(self, afn, title):
        dot = Digraph()

        # Agregar el título si se proporciona
        if title:
            dot.attr(label=title, labelloc='t', fontsize='20')  # 't' para colocar el título arriba

        # Agregar los nodos (estados)
        for state in afn.states:
            if state in afn.final_states:
                dot.node(str(state), shape='doublecircle')  # Estados finales
            else:
                dot.node(str(state))  # Otros estados

        # Agregar las transiciones
        for state, transitions in afn.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    label = symbol if symbol else 'ε'  # Usar 'ε' para transiciones vacías
                    dot.edge(str(state), str(next_state), label=label)

        return dot

    def mostrar_gramatica(self, expr):
        print(f"Gramatica del AFD:")
        print(f'\tEstados: {list(self.afd.states)}')
        print(f'\tSimbolos: {list(self.afd.input_symbols)}')
        print('\tTransiciones: ')
        for state, transition in self.afd.transitions.items():
            for symbol, next_state in transition.items():
                print(f'\t\t {state} -> {symbol}: {next_state}')
        print(f'\tEstado inicial: {self.afd.initial_state}')
        print(f'\tEstado final: {list(self.afd.final_states)}')

        print(f"Gramatica del AFN:")
        print(f'\tEstados : {self.afn.states}')
        print(f'\tSimbolos : {list(self.afn.input_symbols)}')
        print(f'\tEstado inicial: {self.afd.initial_state}')
        print(f'\tEstado final: {self.afd.final_states}')
        print('\tTransiciones: ')
        for state, transition in self.afn.transitions.items():
            for symbol, next_state in transition.items():
                print(f'\t\t {state} -> {symbol}: {next_state}')

        # crear Automata AFD PNG
        dfa_grap = self.generar_diagrama(self.afd, ('Automata AFD: ' + expr))
        dfa_grap.render('Automata Generada AFD', view=True, format='png')

        nfa_grap = self.generar_diagrama_afn(self.afn, ('Automata AFD:' + expr))
        nfa_grap.render('Automata Generada AFN', view=True, format='png')

    def guardar_automata(self):
        def convert_frozenset(obj):
            if isinstance(obj, frozenset):
                return list(obj)  # Convertir frozenset a lista
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        with open('automata.json', 'w') as file:
            data = {
                "AFN": {
                    "Estados": list(self.afn.states),
                    "Simbolos": list(self.afn.input_symbols),
                    "Estado Inicial": self.afn.initial_state,
                    "Estado Final": list(self.afn.final_states),
                    "Transitions": self.afn.transitions
                },
                "AFD": {
                    "Estados": list(self.afd.states),
                    "Simbolos": list(self.afd.input_symbols),
                    "Estado Inicial": self.afd.initial_state,
                    "Estado Final": list(self.afd.final_states),
                    "Transitions": self.afd.transitions
                }
            }
            # Usamos 'default' para manejar cualquier frozenset en las transiciones
            json.dump(data, file, default=convert_frozenset, indent=4)

        print("Automata guardado en automata.json")



def main():
    proyecto = AutomataProject()

    while True:
        print("\nMenú:")
        print("1. Ingresar Expresión Regular")
        print("2. Generar AFN")
        print("3. Convertir a AFD")
        print("4. Validar Cadenas")
        print("5. Mostrar Gramática")
        print("6. Guardar Automata")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            expr = proyecto.ingresar_expresion_regular()
        elif opcion == '2':
            if expr:
                proyecto.generar_afn(expr)
            else:
                print("Primero debe ingresar una expresión regular.")
        elif opcion == '3':
            if proyecto.afn:
                proyecto.convertir_a_afd()
            else:
                print("Primero debe generar un AFN.")
        elif opcion == '4':
            print('\tPara salir escribir exit\t')
            while True:
                cadena = input("\tIngrese la cadena a validar: ")
                if cadena == 'exit':
                    break

                proyecto.validar_cadena(cadena)

        elif opcion == '5':

            if proyecto.afd is not None:
                proyecto.mostrar_gramatica(expr)
            else:
                print("Primero debe ingresar una cadena.")

        elif opcion == '6':
                proyecto.guardar_automata()
        elif opcion == '7':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
