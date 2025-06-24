import reflex as rx

# Configuración de tipografía moderna
class Typography:
    """Configuración de tipografía para toda la aplicación."""
    FONT_FAMILY = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif"
    FONT_WEIGHTS = {
        "light": "300",
        "normal": "400", 
        "medium": "500",
        "semibold": "600",
        "bold": "700"
    }

# Paleta de colores principal
class Color:
    """Paleta de colores para la aplicación."""
    # Escala de azules pastel
    BLUE_100 = "#E0F2FE"
    BLUE_300 = "#7DD3FC"
    BLUE_500 = "#0EA5E9"
    BLUE_700 = "#0369A1"
    
    # Escala de grises y negros (más oscura)
    GRAY_100 = "#1F2937"  # Fondo principal del body - gris oscuro
    GRAY_300 = "#374151"  # Gris medio oscuro
    GRAY_500 = "#6B7280"  # Gris medio
    GRAY_700 = "#9CA3AF"  # Gris claro para texto
    GRAY_900 = "#F9FAFB"  # Texto principal - casi blanco
    WHITE = "#FFFFFF"
    DARK_CARD = "#111827"  # Fondo muy oscuro para tarjetas
    
    # Colores semánticos del proyecto
    PRIMARY = "#004A99"           # Azul principal del proyecto
    PRIMARY_HOVER = "#003875"     # Azul más oscuro para hover
    PRIMARY_LIGHT = "#E3F2FD"     # Azul muy claro para hover en texto
    
    # Colores de estado
    SUCCESS = "#10B981"           # Verde para éxito
    SUCCESS_HOVER = "#059669"     # Verde más oscuro
    WARNING = "#F59E0B"           # Amarillo para advertencias
    WARNING_HOVER = "#D97706"     # Amarillo más oscuro
    DANGER = "#EF4444"            # Rojo para peligro/eliminar
    DANGER_HOVER = "#DC2626"      # Rojo más oscuro
    
    # Colores de superficie
    SURFACE_LIGHT = "#F3F4F6"     # Gris muy claro para hover en tablas
    BORDER_LIGHT = "#E5E7EB"      # Bordes sutiles

# Estilos de botones centralizados
class ButtonStyle:
    """Estilos de botones reutilizables."""
    
    @staticmethod
    def primary(**kwargs):
        """Botón principal del proyecto."""
        return {
            "bg": Color.PRIMARY,
            "color": Color.WHITE,
            "_hover": {"bg": Color.PRIMARY_HOVER},
            "border": "none",
            **kwargs
        }
    
    @staticmethod
    def secondary(**kwargs):
        """Botón secundario con outline."""
        return {
            "variant": "outline",
            "border_color": Color.PRIMARY,
            "color": Color.PRIMARY,
            "_hover": {
                "bg": Color.PRIMARY_LIGHT,
                "border_color": Color.PRIMARY_HOVER,
            },
            **kwargs
        }
    
    @staticmethod
    def danger(**kwargs):
        """Botón de peligro para acciones destructivas."""
        return {
            "bg": Color.DANGER,
            "color": Color.WHITE,
            "_hover": {"bg": Color.DANGER_HOVER},
            "border": "none",
            **kwargs
        }
    
    @staticmethod
    def success(**kwargs):
        """Botón de éxito."""
        return {
            "bg": Color.SUCCESS,
            "color": Color.WHITE,
            "_hover": {"bg": Color.SUCCESS_HOVER},
            "border": "none",
            **kwargs
        }

# Estilos de componentes específicos
class ComponentStyle:
    """Estilos para componentes específicos."""
    
    # Estilos para tablas
    TABLE = {
        "variant": "surface",
        "width": "100%",
        "bg": Color.WHITE,
        "border": f"1px solid {Color.GRAY_500}",
        "border_radius": "8px",
        "size": "3",
    }
    
    TABLE_HEADER = {
        "color": Color.GRAY_900,
        "bg": Color.GRAY_300,
    }
    
    TABLE_CELL = {
        "color": Color.GRAY_900,
        "bg": Color.WHITE,
        "border_bottom": f"1px solid {Color.GRAY_500}",
        "padding": "12px",
    }
    
    TABLE_ROW_HOVER = {
        "_hover": {"bg": Color.SURFACE_LIGHT},
    }
    
    # Estilos para formularios
    FORM_INPUT = {
        "bg": Color.GRAY_300,
        "color": Color.GRAY_900,
        "border_color": Color.GRAY_500,
        "_placeholder": {"color": Color.GRAY_900, "opacity": "0.6"},
        "_hover": {"border_color": Color.BLUE_300},
        "_focus": {
            "border_color": Color.BLUE_300, 
            "box_shadow": f"0 0 0 1px {Color.BLUE_300}"
        },
    }
    
    # Estilos específicos para dropdowns/selects
    FORM_SELECT = {
        "bg": Color.GRAY_300,
        "color": Color.GRAY_900,
        "border_color": Color.GRAY_500,
        "_placeholder": {"color": Color.GRAY_900, "opacity": "0.6"},
        "_hover": {"border_color": Color.BLUE_300},
        "_focus": {
            "border_color": Color.BLUE_300, 
            "box_shadow": f"0 0 0 1px {Color.BLUE_300}"
        },
    }
    
    FORM_LABEL = {
        "font_size": "sm",
        "font_weight": "medium",
        "color": Color.GRAY_900,
        "margin_bottom": "4px",
    }
    
    # Estilos para modales
    MODAL = {
        "bg": Color.DARK_CARD,
        "border": f"1px solid {Color.GRAY_500}",
        "border_radius": "12px",
        "box_shadow": "2xl",
    }
    
    MODAL_HEADER = {
        "color": Color.GRAY_900,
        "font_weight": Typography.FONT_WEIGHTS["semibold"],
        "border_bottom": f"1px solid {Color.GRAY_500}",
        "padding_bottom": "16px",
        "margin_bottom": "16px",
    }
    
    MODAL_FOOTER = {
        "border_top": f"1px solid {Color.GRAY_500}",
        "padding_top": "16px",
        "margin_top": "16px",
    }

    # Estilos específicos para tablas de cursos
    COURSE_TABLE = {
        "variant": "surface",
        "width": "100%",
        "bg": Color.WHITE,
        "border": f"1px solid {Color.GRAY_500}",
        "border_radius": "8px",
        "size": "3",
    }
    
    COURSE_TABLE_HEADER = {
        "color": Color.GRAY_900,
        "bg": Color.GRAY_300,
        "font_weight": Typography.FONT_WEIGHTS["semibold"],
        "font_family": Typography.FONT_FAMILY,
        "padding": "16px 12px",
        "text_align": "left",
        "border_bottom": f"2px solid {Color.GRAY_500}",
    }
    
    COURSE_TABLE_CELL = {
        "color": "#000000",  # Negro explícito para máximo contraste
        "bg": Color.WHITE,
        "font_family": Typography.FONT_FAMILY,
        "padding": "12px",
        "border_bottom": f"1px solid {Color.GRAY_500}",
        "font_weight": Typography.FONT_WEIGHTS["normal"],
        "vertical_align": "middle",
    }
    
    COURSE_TABLE_ROW_HOVER = {
        "_hover": {"bg": Color.SURFACE_LIGHT},
    }
    
    # Container para tablas de cursos
    COURSE_TABLE_CONTAINER = {
        "width": "100%",
        "overflow_x": "auto",
        "border_radius": "12px",
        "box_shadow": "lg",
    }

# Estilos globales para la aplicación
STYLESHEET = {
    # Importar fuente moderna de Google Fonts
    "@import": "url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap')",
    
    "body": {
        "background_color": Color.GRAY_100,  # Fondo oscuro
        "color": Color.GRAY_900,  # Texto claro
        "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif",
    },
    "h1, h2, h3, h4, h5, h6": {
        "color": Color.GRAY_900,  # Títulos en claro
        "font_family": "'Inter', sans-serif",
        "font_weight": "600",
    },
    "a": {
        "text_decoration": "none",
        "color": "inherit",
    },
    # Aplicar fondo oscuro a todos los contenedores principales
    ".chakra-stack": {
        "background_color": "transparent",
    },
    # Estilos más específicos para dropdowns
    "select": {
        "background_color": f"{Color.GRAY_300} !important",
        "color": f"{Color.GRAY_900} !important",
    },
    "select option": {
        "background_color": f"{Color.GRAY_300} !important",
        "color": f"{Color.GRAY_900} !important",
        "font_family": "'Inter', sans-serif",
    },
    "select option:hover": {
        "background_color": f"{Color.BLUE_300} !important",
        "color": f"{Color.GRAY_900} !important",
    },
    "select option:checked": {
        "background_color": f"{Color.BLUE_300} !important",
        "color": f"{Color.GRAY_900} !important",
    },
    # Estilos para el componente Select de Chakra UI
    ".chakra-select__wrapper": {
        "background_color": f"{Color.GRAY_300} !important",
    },
    ".chakra-select": {
        "background_color": f"{Color.GRAY_300} !important",
        "color": f"{Color.GRAY_900} !important",
    },
    # CSS personalizado para forzar el estilo en dropdowns
    ":root": {
        "--select-bg": Color.GRAY_300,
        "--select-color": Color.GRAY_900,
        "--select-hover-bg": Color.BLUE_300,
    }
}

# Configuración del tema de Chakra UI
chakra_theme_config = {
    "colors": {
        "primary": {
            100: Color.BLUE_100,
            300: Color.BLUE_300,
            500: Color.BLUE_500,
            700: Color.BLUE_700,
        },
        "gray": {
            100: Color.GRAY_100,
            300: Color.GRAY_300,
            500: Color.GRAY_500,
            700: Color.GRAY_700,
            900: Color.GRAY_900,
        },
    },
    "components": {
        "Button": {
            "baseStyle": {
                "_hover": {
                    "transform": "scale(1.03)",
                },
            },
            "variants": {
                "solid": {
                    "bg": "primary.500",
                    "color": "white",
                    "_hover": {
                        "bg": "primary.700",
                    },
                },
                "outline": {
                    "borderColor": "primary.500",
                    "color": "primary.500",
                    "_hover": {
                        "bg": "primary.100",
                    },
                },
            },
        },
        "Heading": {
            "baseStyle": {
                "font_weight": "bold",
            },
        },
    },
} 

# Funciones helper para crear componentes con estilos consistentes
def create_button(text: str, button_type: str = "primary", on_click=None, **kwargs):
    """Crea un botón con estilos consistentes del tema."""
    style_map = {
        "primary": ButtonStyle.primary,
        "secondary": ButtonStyle.secondary,
        "danger": ButtonStyle.danger,
        "success": ButtonStyle.success,
    }
    
    style_func = style_map.get(button_type, ButtonStyle.primary)
    button_style = style_func(
        font_family=Typography.FONT_FAMILY,
        font_weight=Typography.FONT_WEIGHTS["medium"],
        **kwargs
    )
    
    return rx.button(
        text,
        on_click=on_click,
        **button_style
    )

def create_course_table_header(headers: list):
    """Crea un header estandarizado para tablas de cursos."""
    return rx.table.row(
        *[
            rx.table.column_header_cell(
                header,
                **ComponentStyle.COURSE_TABLE_HEADER,
            )
            for header in headers
        ]
    )

def create_course_table_cell(content, **additional_props):
    """Crea una celda estandarizada para tablas de cursos."""
    cell_style = {**ComponentStyle.COURSE_TABLE_CELL, **additional_props}
    return rx.table.cell(content, **cell_style)

def create_course_table_row(cells_content: list, action_buttons=None, **additional_props):
    """Crea una fila estandarizada para tablas de cursos."""
    cells = [create_course_table_cell(content) for content in cells_content]
    
    if action_buttons:
        cells.append(
            rx.table.cell(
                action_buttons,
                **ComponentStyle.COURSE_TABLE_CELL,
            )
        )
    
    row_style = {**ComponentStyle.COURSE_TABLE_ROW_HOVER, **additional_props}
    return rx.table.row(*cells, **row_style)

def create_custom_dropdown_css():
    """Crea CSS personalizado para mejorar el estilo de los dropdowns."""
    css_content = f"""
    <style>
        /* Estilos para dropdowns nativos */
        select {{
            background-color: {Color.GRAY_300} !important;
            color: {Color.GRAY_900} !important;
            border-color: {Color.GRAY_500} !important;
        }}
        
        select option {{
            background-color: {Color.GRAY_300} !important;
            color: {Color.GRAY_900} !important;
            padding: 8px !important;
        }}
        
        select option:hover {{
            background-color: {Color.BLUE_300} !important;
            color: {Color.GRAY_900} !important;
        }}
        
        select option:checked {{
            background-color: {Color.BLUE_300} !important;
            color: {Color.GRAY_900} !important;
        }}
        
        /* Estilos específicos para Chakra UI Select */
        .chakra-select__wrapper select {{
            background-color: {Color.GRAY_300} !important;
            color: {Color.GRAY_900} !important;
        }}
        
        .chakra-select__wrapper select option {{
            background-color: {Color.GRAY_300} !important;
            color: {Color.GRAY_900} !important;
        }}
        
        /* HEADER AG GRID - CORRECCIÓN COMPLETA */
        .ag-theme-alpine .ag-header,
        .ag-theme-alpine .ag-header-container,
        .ag-theme-alpine .ag-header-viewport {{
            background-color: #ffffff !important;
            height: 30px !important;
            min-height: 30px !important;
            max-height: 30px !important;
            border-bottom: 1px solid #d1d5db !important;
        }}
        
        .ag-theme-alpine .ag-header-row {{
            height: 30px !important;
            min-height: 30px !important;
            max-height: 30px !important;
            background-color: #ffffff !important;
        }}
        
        .ag-theme-alpine .ag-header-cell {{
            background-color: #ffffff !important;
            border-right: 1px solid #e5e7eb !important;
            height: 30px !important;
            min-height: 30px !important;
            max-height: 30px !important;
            padding: 0 4px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-sizing: border-box !important;
        }}
        
        .ag-theme-alpine .ag-header-cell-text {{
            font-weight: 600 !important;
            color: #374151 !important;
            font-size: 11px !important;
            line-height: 1.2 !important;
            text-align: center !important;
            margin: 0 !important;
            padding: 0 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}
        
        .ag-theme-alpine .ag-header-cell-menu-button {{
            width: 12px !important;
            height: 12px !important;
            margin-left: 2px !important;
            opacity: 0.7 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
        
        .ag-theme-alpine .ag-header-cell-menu-button:hover {{
            opacity: 1 !important;
        }}
        
        /* Eliminar hover azul */
        .ag-theme-alpine .ag-header-cell-sortable:hover {{
            background-color: #f8f9fa !important;
        }}
        
        .ag-theme-alpine .ag-header-cell-sorted-asc,
        .ag-theme-alpine .ag-header-cell-sorted-desc {{
            background-color: #f1f3f4 !important;
        }}
        
        /* Forzar altura en contenedores padre */
        .ag-theme-alpine .ag-pinned-left-header,
        .ag-theme-alpine .ag-pinned-right-header {{
            background-color: #ffffff !important;
            height: 30px !important;
        }}
        
        /* Eliminar padding extra */
        .ag-theme-alpine .ag-header-cell-resize {{
            height: 30px !important;
        }}
    </style>
    """
    return rx.html(css_content)

def create_ag_grid_actions_script():
    """Crea el JavaScript necesario para manejar acciones en AG Grid."""
    return rx.html("""
    <script>
        // Renderer personalizado para botones de acción en AG Grid
        class ActionsCellRenderer {
            init(params) {
                this.eGui = document.createElement('div');
                this.eGui.innerHTML = `
                    <div style="display: flex; gap: 8px; align-items: center; height: 100%; justify-content: center;">
                        <button class="ag-grid-btn ag-grid-btn-secondary" data-action="edit" data-curso-id="${params.data.id}">
                            Editar
                        </button>
                        <button class="ag-grid-btn ag-grid-btn-danger" data-action="delete" data-curso-id="${params.data.id}">
                            Eliminar
                        </button>
                    </div>
                `;
                
                // Agregar event listeners
                const editBtn = this.eGui.querySelector('[data-action="edit"]');
                const deleteBtn = this.eGui.querySelector('[data-action="delete"]');
                
                if (editBtn) {
                    editBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        // Intentar múltiples formas de comunicación con Reflex
                        try {
                            // Método 1: Trigger Reflex state update directly
                            if (window.__reflex_state__) {
                                window.__reflex_state__.handle_ag_grid_edit(params.data);
                            }
                            
                            // Método 2: Custom event para Reflex
                            const event = new CustomEvent('curso-edit', { 
                                detail: { 
                                    type: 'edit',
                                    id: params.data.id,
                                    curso: params.data 
                                } 
                            });
                            window.dispatchEvent(event);
                            
                            // Método 3: Backend call si está disponible
                            if (window.handleEditCurso) {
                                window.handleEditCurso(params.data);
                            }
                            
                            console.log('Edit button clicked for course:', params.data);
                        } catch (error) {
                            console.error('Error handling edit:', error);
                        }
                    });
                }
                
                if (deleteBtn) {
                    deleteBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        // Intentar múltiples formas de comunicación con Reflex
                        try {
                            // Método 1: Trigger Reflex state update directly
                            if (window.__reflex_state__) {
                                window.__reflex_state__.handle_ag_grid_delete(params.data.id);
                            }
                            
                            // Método 2: Custom event para Reflex
                            const event = new CustomEvent('curso-delete', { 
                                detail: { 
                                    type: 'delete',
                                    id: params.data.id 
                                } 
                            });
                            window.dispatchEvent(event);
                            
                            // Método 3: Backend call si está disponible
                            if (window.handleDeleteCurso) {
                                window.handleDeleteCurso(params.data.id);
                            }
                            
                            console.log('Delete button clicked for course ID:', params.data.id);
                        } catch (error) {
                            console.error('Error handling delete:', error);
                        }
                    });
                }
            }
            
            getGui() {
                return this.eGui;
            }
            
            destroy() {
                // Limpiar event listeners si es necesario
            }
        }
        
        // Registrar el renderer cuando AG Grid esté disponible
        function registerActionsCellRenderer() {
            if (typeof agGrid !== 'undefined') {
                agGrid.registerCellRenderer('actionsCellRenderer', ActionsCellRenderer);
            } else if (window.agGrid) {
                window.agGrid.registerCellRenderer('actionsCellRenderer', ActionsCellRenderer);
            } else {
                // Intentar de nuevo en 100ms
                setTimeout(registerActionsCellRenderer, 100);
            }
        }
        
        // Ejecutar cuando el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', registerActionsCellRenderer);
        } else {
            registerActionsCellRenderer();
        }
    </script>
    
    <style>
        .ag-grid-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s ease;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }
        
        .ag-grid-btn-secondary {
            background-color: transparent;
            border: 1px solid #004A99;
            color: #004A99;
        }
        
        .ag-grid-btn-secondary:hover {
            background-color: #E3F2FD;
            border-color: #003875;
            transform: translateY(-1px);
        }
        
        .ag-grid-btn-danger {
            background-color: #EF4444;
            color: white;
            border: 1px solid #EF4444;
        }
        
        .ag-grid-btn-danger:hover {
            background-color: #DC2626;
            border-color: #DC2626;
            transform: translateY(-1px);
        }
        
        /* Estilos para AG Grid */
        .ag-theme-alpine {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }
        
        .ag-theme-alpine .ag-header-cell-text {
            font-weight: 600;
            color: #374151;
        }
        
        .ag-theme-alpine .ag-cell {
            line-height: 1.5;
        }
        
        .ag-theme-alpine .ag-row-hover {
            background-color: #F3F4F6;
        }
    </style>
    """)

def create_course_table(headers: list, rows_data: list, render_row_func=None):
    """Crea una tabla completa de cursos con estilos estandarizados."""
    return rx.table.root(
        rx.table.header(
            create_course_table_header(headers)
        ),
        rx.table.body(
            rx.foreach(rows_data, render_row_func) if render_row_func else None
        ),
        **ComponentStyle.COURSE_TABLE,
    ) 