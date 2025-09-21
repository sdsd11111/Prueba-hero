# 🍽️ La Herencia - Restaurante Web Application

Una aplicación web completa para el restaurante "La Herencia" con frontend dinámico, backend con panel de control administrativo y funcionalidad de slider/carrusel para mostrar platos del día.

## 🌟 Características Principales

### Frontend
- **Header dinámico y responsive** con navegación completa
- **Hero section fullscreen** con título principal "La Herencia"
- **Slider/carrusel automático** para mostrar hasta 3 platos del día
- **Diseño responsive** optimizado para móviles y desktop
- **Animaciones y transiciones suaves** para una experiencia premium
- **Navegación por teclado y gestos táctiles** (swipe en móviles)

### Backend
- **Panel de control administrativo** con autenticación segura
- **Gestión completa de platos del día** (crear, editar, eliminar, activar/desactivar)
- **Subida de imágenes** para cada plato
- **API RESTful** para comunicación frontend-backend
- **Base de datos SQLite** para persistencia de datos
- **Límite de 3 platos activos** simultáneamente

### Funcionalidades del Slider
- **Auto-slide cada 5 segundos** cuando hay múltiples platos
- **Controles manuales** (botones anterior/siguiente)
- **Indicadores de posición** (dots) clickeables
- **Pausa automática** al hacer hover sobre el contenido
- **Soporte para navegación por teclado** (flechas izquierda/derecha)
- **Gestos de swipe** en dispositivos móviles

## 🚀 URLs de Acceso

- **Página Principal**: https://19hninc0zd15.manus.space
- **Panel Administrativo**: https://19hninc0zd15.manus.space/admin.html

## 🔐 Credenciales de Administrador

- **Usuario**: `La herencia`
- **Contraseña**: `laherencia123`

## 📋 Platos del Día Precargados

La aplicación viene con 3 platos de ejemplo:

1. **Pechuga gratinada en salsa de champiñones** - $13.00
   - Pechuga gratinada en salsa de champiñones con papas fritas, ensalada fresca, cheesecake de maracuyá y una bebida.

2. **Hamburguesa La Herencia** - $11.50
   - Hamburguesa de carne, cheddar y tocino con papas fritas, un cheesecake de maracuyá y una bebida.

3. **Lasaña mixta** - $11.50
   - Lasaña mixta acompañada de pan de ajo, una ensalada fresca, un cheesecake de maracuyá y una bebida.

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web de Python
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos ligera
- **Flask-CORS** - Manejo de CORS
- **Werkzeug** - Utilidades WSGI

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos avanzados con Flexbox/Grid
- **JavaScript ES6+** - Funcionalidad interactiva
- **Google Fonts** - Tipografías Playfair Display e Inter
- **Responsive Design** - Compatible con todos los dispositivos

## 📁 Estructura del Proyecto

```
la_herencia_backend/
├── src/
│   ├── models/
│   │   ├── user.py          # Modelo de usuario
│   │   └── plato.py         # Modelo de platos del día
│   ├── routes/
│   │   ├── user.py          # Rutas de usuario
│   │   └── platos.py        # Rutas de platos y admin
│   ├── static/
│   │   ├── index.html       # Página principal
│   │   ├── admin.html       # Panel administrativo
│   │   └── uploads/         # Directorio de imágenes
│   ├── database/
│   │   └── app.db          # Base de datos SQLite
│   └── main.py             # Punto de entrada de la aplicación
├── venv/                   # Entorno virtual de Python
├── requirements.txt        # Dependencias de Python
├── load_sample_data.py     # Script para cargar datos de ejemplo
└── README.md              # Esta documentación
```

## 🎯 Funcionalidades del Panel Administrativo

### Autenticación
- Login seguro con credenciales específicas
- Sesiones persistentes
- Logout automático por seguridad

### Gestión de Platos
- **Crear nuevos platos** con título, descripción, precio e imagen
- **Editar platos existentes** con modal intuitivo
- **Activar/Desactivar platos** sin eliminarlos
- **Eliminar platos** con confirmación
- **Subida de imágenes** con preview instantáneo
- **Límite de 3 platos activos** para mantener el diseño

### Validaciones
- Máximo 3 platos del día activos simultáneamente
- Validación de tipos de archivo para imágenes
- Campos obligatorios en formularios
- Manejo de errores con mensajes informativos

## 🎨 Características de Diseño

### Paleta de Colores
- **Primario**: Gradiente naranja-rojo (#ff6b6b a #ee5a24)
- **Secundario**: Dorado (#ffd700) para precios y acentos
- **Neutros**: Grises y blancos para texto y fondos
- **Fondo Hero**: Gradiente azul-gris con efectos animados

### Tipografía
- **Playfair Display**: Títulos elegantes y precios
- **Inter**: Texto de cuerpo y navegación

### Efectos Visuales
- **Backdrop blur**: Efectos de desenfoque en elementos flotantes
- **Animaciones CSS**: Transiciones suaves y micro-interacciones
- **Hover effects**: Estados interactivos en botones y enlaces
- **Loading states**: Indicadores de carga para mejor UX

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 768px - Layout completo con navegación horizontal
- **Tablet**: 768px - 480px - Navegación adaptada
- **Mobile**: < 480px - Menú hamburguesa y layout vertical

### Adaptaciones Móviles
- **Menú hamburguesa** para navegación en móviles
- **Gestos de swipe** para el slider
- **Botones táctiles** optimizados para dedos
- **Tipografía escalable** con clamp() CSS

## 🔧 API Endpoints

### Públicos
- `GET /api/platos` - Obtener platos del día activos

### Administrativos (requieren autenticación)
- `POST /api/login` - Iniciar sesión
- `POST /api/logout` - Cerrar sesión
- `GET /api/check-auth` - Verificar autenticación
- `GET /api/admin/platos` - Obtener todos los platos
- `POST /api/admin/platos` - Crear nuevo plato
- `PUT /api/admin/platos/{id}` - Actualizar plato
- `DELETE /api/admin/platos/{id}` - Eliminar plato
- `PUT /api/admin/platos/{id}/toggle` - Activar/desactivar plato
- `POST /api/upload-image` - Subir imagen

## 🚀 Instalación y Desarrollo Local

### Prerrequisitos
- Python 3.11+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd la_herencia_backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python src/main.py
   ```

5. **Cargar datos de ejemplo** (opcional)
   ```bash
   python load_sample_data.py
   ```

6. **Acceder a la aplicación**
   - Página principal: http://localhost:5000
   - Panel admin: http://localhost:5000/admin.html

## 🎯 Casos de Uso

### Para Clientes
1. **Visualizar platos del día** en la página principal
2. **Navegar entre opciones** usando el slider automático
3. **Ver detalles completos** de cada plato (título, descripción, precio)
4. **Acceder desde cualquier dispositivo** con diseño responsive

### Para Administradores
1. **Gestionar el menú diario** desde el panel de control
2. **Subir imágenes atractivas** para cada plato
3. **Activar/desactivar platos** según disponibilidad
4. **Mantener máximo 3 opciones** para optimizar la experiencia

## 🔒 Seguridad

- **Autenticación basada en sesiones** para el panel administrativo
- **Validación de tipos de archivo** para subida de imágenes
- **Sanitización de inputs** para prevenir inyecciones
- **Límites de tamaño** para archivos subidos
- **Nombres de archivo seguros** con timestamps únicos

## 🌟 Características Avanzadas

### Slider Inteligente
- **Detección automática** del número de platos
- **Comportamiento adaptativo**: sin controles si hay 1 plato, slider completo si hay múltiples
- **Auto-pausa** al interactuar manualmente
- **Indicadores visuales** del plato activo

### Experiencia de Usuario
- **Estados de carga** informativos
- **Mensajes de error** amigables
- **Confirmaciones** para acciones destructivas
- **Feedback visual** inmediato en todas las interacciones

## 📈 Rendimiento

- **Imágenes optimizadas** con compresión automática
- **CSS y JS minificados** para carga rápida
- **Lazy loading** para contenido no crítico
- **Cache de navegador** para recursos estáticos

## 🎨 Personalización

El diseño está construido con CSS custom properties (variables) que facilitan la personalización:

```css
:root {
  --primary-color: #ff6b6b;
  --secondary-color: #ffd700;
  --text-color: #333;
  --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 📞 Soporte

Para soporte técnico o consultas sobre la aplicación, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ para La Herencia Restaurante**
