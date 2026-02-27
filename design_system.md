# Sistema de Diseño de Alergenu

Este documento sirve como la **Única Fuente de Verdad** para el diseño de la aplicación.

## Principios Fundamentales
1.  **Rounding Extremo**: La forma primaria de la aplicación es `rounded-full`.
    -   **Botones**: Siempre `rounded-full`.
    -   **Inputs pequeños**: `rounded-full`.
    -   **Contenedores**: `rounded-3xl` (o `2xl` mínimo) para eliminar esquinas rectas. NUNCA usar colores de fondo (fill/pastel). Fondo BLANCO o TRANSPARENTE.
2.  **Cero Variantes**: Se evitan variantes redundantes. El botón "Perfecto" es el comportamiento por defecto.
3.  **Tipografía SemiBold**: Los elementos interactivos (botones) usan `font-semibold` para mantener la jerarquía sin ser agresivos.

## Componentes

### Botones (`Button`)

El componente `Button` ha sido simplificado radicalmente.

-   **Componente**: `src/components/ui/button.tsx`
-   **DEFAULT (Primary Actions)**:
    -   Sin props de tamaño: `<Button>Texto</Button>`
    -   **Specs**: `h-14`, `rounded-full`, `px-8`, `text-lg`, `font-bold`.
    -   Uso: **PARA TODO**. Es el botón estándar de la aplicación.
### Inputs
-   **Estilo Base**: `h-14`, `rounded-full`, `px-6`, `border-input`, `bg-background`.
-   **Tipografía**: `text-primary` (Azul corporativo) al escribir, `text-base` o `text-sm` (desktop).
-   **Focus**: `ring-2`, `ring-ring` (Azul corporativo).

### Google Button
-   Debe imitar el estilo del botón `default` pero con estilo `outline` o borde gris suave.
-   **Specs**: `h-14`, `rounded-full`, `w-full`, `font-bold`.
-   **`size="lg"` (Medium/Secondary)**:
    -   **Specs**: `h-11`, `rounded-full`, `px-8`, `text-base`, `font-bold`.
    -   Uso: Botones de cabecera, acciones secundarias importantes o cuando el Gigante es excesivo.

### Content Guidelines
> [!IMPORTANT]
> **NEVER use Title Case** for sentences, headers, or buttons.
-   **Correct**: "Guardar cambios", "Crear nuevo plato", "Volver al menú"
-   **Incorrect**: "Guardar Cambios", "Crear Nuevo Plato", "Volver Al Menú"
-   Only the first letter of the sentence and proper nouns should be capitalized.

### Pop-ups & Dialogs
Standardize the appearance of modals and alert dialogs.

- **Container**:
  - `rounded-2xl`
  - `bg-white`
  - `p-6` or `p-8`
  - `max-w-md` or `max-w-lg` (depending on content)
- **Icons (Standalone)**:
  - **Placement**: ALWAYS **above** the title (centered). Never to the side.
  - **Size**: Standardized to `h-8 w-8` (32px).
  - **Style**: Often accompanied by a rounded background (e.g., `bg-red-100` for alerts).
- **Typography**:
  - **Title**: `text-2xl`, `font-bold`, `text-gray-900`. **Sentence case only.**
  - **Description**: `text-base`, `text-gray-500`, `mt-2`, `leading-relaxed`.
- **Actions (Footer)**:
  - **Layout**: Right-aligned on desktop, Full-width `flex-col` on mobile.
  - **Primary Button**: `rounded-full`, `h-14`, `font-bold`, `text-lg`.
  - **Secondary Button**: `variant="outline"`, `rounded-full`, `h-14`, `font-bold`, `text-lg`, `border-gray-200`.
- **Example Structure**:
```tsx
<DialogContent className="sm:max-w-[425px] p-0 overflow-hidden rounded-2xl gap-0">
    <div className="p-6">
        <DialogHeader className="mb-4">
            <DialogTitle className="text-xl font-bold text-left">Confirmar acción</DialogTitle>
            <DialogDescription className="text-base text-gray-500 text-left">
                ¿Estás seguro de que quieres continuar? Esta acción no se puede deshacer.
            </DialogDescription>
        </DialogHeader>
        <DialogFooter className="flex-col sm:flex-row gap-2 mt-6">
             <Button variant="ghost" className="rounded-full h-12 font-bold">Cancelar</Button>
             <Button className="rounded-full h-12 font-bold bg-black text-white">Confirmar</Button>
        </DialogFooter>
    </div>
</DialogContent>
```

### Specialized Buttons

#### "Back" Button (Volver)
Used for navigation back to the previous context.
- **Component**: `Link` (pseudo-button) or `Button`.
- **Style**:
  - Background: `bg-gray-100` (hover: `bg-gray-200`)
  - Text: `text-gray-600`
  - Font: `font-semibold`
  - Radius: `rounded-full`
  - Height: `h-10`
  - Padding: `px-4 py-2`
  - Icon: `<ArrowLeft className="h-4 w-4" />` (Left aligned)
  - Transition: `transition-colors`
- **Example**:
```tsx
<Link href="..." className="inline-flex items-center gap-x-2 text-gray-600 font-semibold rounded-full bg-gray-100 hover:bg-gray-200 px-4 py-2 transition-colors h-10">
  <ArrowLeft className="h-4 w-4" />
  Volver
</Link>
```

### Select / Dropdowns
Standardize the appearance of select dropdowns using shadcn's Select component.

- **Component**: Use `Select` from `@/components/ui/select`
- **Trigger**:
  - `rounded-full` (consistent with inputs)
  - `h-11` (standard input height)
  - `border border-gray-300`
  - `focus:ring-2 focus:ring-blue-600`
- **Label**:
  - Use `Label` component from `@/components/ui/label`
  - `text-sm font-medium text-gray-700 mb-2`
- **Example**:
```tsx
<div>
  <Label htmlFor="filter-status">Estado</Label>
  <Select value={status} onValueChange={setStatus}>
    <SelectTrigger id="filter-status" className="w-full rounded-full">
      <SelectValue />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="all">Todos</SelectItem>
      <SelectItem value="active">Activos</SelectItem>
    </SelectContent>
  </Select>
</div>
```

### Pop-ups & Dialogs
Standardize the appearance of modals and alert dialogs.

- **Container**:
  - Radius: `rounded-2xl` (matches cards)
  - Background: `bg-white`
  - Padding: `p-6` (standard)
### Typography
- **Font Family**: Manrope, sans-serif (Primary)
- **Headings**:
  - **H1 (Page Title)**:
    - Font: `Manrope`
    - Weight: `800` (ExtraBold)
    - Size: `2.5rem` (Desktop) / `2rem` (Mobile)
    - Line Height: `110%`
    - Letter Spacing: `-0.1rem`
  - H2: `text-xl font-semibold` (Section titles)
  - H3: `text-lg font-medium` (Subsection titles)
- **Body / Paragraphs**:
  - Font: `Manrope`
  - Weight: `400` (Regular)
  - Size: `0.9375rem` (15px)
  - Line Height: `141%`
  - Color: `text-gray-900` (Primary) or `text-gray-600` (Secondary)
- **Font Weights**:
  - **H1 ONLY**: `font-extrabold` (800).
  - **UI Elements**: `font-semibold` (600) max.
  - **Body**: `font-normal` (400).
- **Buttons** (Footer):
  - Alignment: Right-aligned or Full-width (mobile).
  - Primary Action (e.g., Save/Confirm):
    - Style: Standard Primary Button (`bg-black`, `rounded-full`, `h-14` or `h-10` depending on context, `font-semibold`).
    - Destructive Action: `bg-red-600 hover:bg-red-700`
  - Secondary Action (e.g., Cancel):
    - Style: Ghost or Outline (`variant="ghost"` or `variant="outline"`), `rounded-full`, `font-semibold`.
    - **IMPORTANT**: DO NOT use "X" icons to close modals. ALWAYS provide a explicit "Cancelar" or "Cerrar" button.
-   **Specs**: `h-14`, `rounded-full`, `px-10`, `text-lg`, `font-semibold`.
-   **Specs**: `h-11`, `rounded-full`, `px-10`, `text-base`, `font-semibold`.
-   **Specs**: `h-9`, `rounded-full`, `px-6`, `text-sm`, `font-semibold`.

### Colores (Brand)
-   **Brand Blue**: `#2563EB` (Tailwind `bg-blue-600` hover `bg-blue-700`)
-   **Dark Blue**: (Tailwind `bg-blue-800` hover `bg-blue-900`)
-   **Teal**: `#008AA0` (Tailwind `bg-[#008AA0]` hover `bg-[#006F80]`)
-   **Yellow (Warning/Alert)**: `#FFA32B` (Tailwind `bg-[#FFA32B]`). Usar con opacidad para fondos.
-   **Destructive**: `bg-destructive` (Rojo estándar de shadcn).
    
### Prohibiciones Explícitas
-   **NO USAR COLORES PASTEL**: Prohibido usar `bg-blue-50`, `bg-green-100`, etc. en contenedores grandes.
-   **NO USAR FLECHAS "ATRÁS"**: Usar un botón de "Cancelar" explícito.
-   **NO ICONOS EN BOTONES**: Salvo excepciones justificadas (ej: "Añadir +"), los botones de acción principal NO deben llevar iconos decorativos.

### Tipografía (Escala)
-   **Display**: `text-5xl` / `text-6xl` (Hero titles).
-   **H1**: `text-4xl` (`font-extrabold`).
-   **H2**: `text-3xl` (`font-extrabold`).
-   **Body Large**: `text-lg` / `text-xl` (Lead text).
-   **Body**: `text-base` (Párrafos estándar).
-   **Small**: `text-sm` (Metadatos, descripciones secundarias).

### Sombras y Efectos
> [!IMPORTANT]
> **NO Sombras Paralelas (Drop Shadows)**.
> - El diseño debe ser plano (flat) y limpio.
> - No usar `shadow-sm`, `shadow-md`, `shadow-lg`, etc.

### Alertas y Notificaciones (Master Token)
Patrón oficial para avisos importantes, validaciones o mensajes de estado.

-   **Contenedor**:
    -   `bg-blue-50`
    -   `border border-blue-100` (sutil)
    -   `rounded-3xl`
    -   `p-8`
    -   `flex flex-col items-center text-center`
-   **Icono**:
    -   `w-12 h-12`
    -   `bg-white`
    -   `rounded-full`
    -   `text-blue-600`
    -   siempre centrado arriba con `mb-4`
-   **Texto**:
    -   **Título**: `text-xl font-bold text-blue-900 mb-2`
    -   **Cuerpo**: `text-base text-blue-700 leading-relaxed`

---

### Iconos de Alérgenos

**Componente Oficial**: `AllergenIconDisplay` (ubicado en `src/components/menu/allergen-icon-display.tsx`).
> [!CAUTION]
> **PROHIBIDO** crear iconos de alérgenos manualmente con `div` + `svg`. 
> **PROHIBIDO** usar imágenes (PNG, JPG, WEBP) para representar alérgenos. Solo se permiten los componentes SVG dinámicos del sistema.

#### Especificaciones Generales
-   **Tamaño del Contenedor**: `w-6 h-6` (24px).
-   **Tamaño del Icono (SVG)**: 80% del contenedor (`w-[80%] h-[80%]`).
-   **Centrado**: Flexbox absoluto (`flex items-center justify-center`).

#### Variantes

| Estado | Fondo | Borde | Color Icono |
| :--- | :--- | :--- | :--- |
| **Contiene** | `bg-[color]` (Sólido) | `border-2 border-[color]` (Sólido) | `text-white` |
| **Trazas** | `bg-transparent` | `border-2 border-dashed border-[color]` | `text-[color]` |

> [!IMPORTANT]
> El borde de `Contiene` es necesario para igualar el "box-sizing" con `Trazas` y evitar saltos de píxel en el alineamiento.

#### Mapeo de Iconos (Lucide React)

El sistema utiliza iconos específicos de `lucide-react`. No se permite el uso de otros iconos.

| Alérgeno (ID) | Icono Lucide | Color (Hex) | Notas |
| :--- | :--- | :--- | :--- |
| `gluten` | `Wheat` | `#CFA15A` | - |
| `leche` | `Milk` | `#3B82F6` | - |
| `huevos` | `Egg` | `#D97706` | - |
| `pescado` | `Fish` | `#3A5E73` | - |
| `crustaceos` | `Shell` | `#A23C3C` | - |
| `moluscos` | `Shell` | `#047857` | Mismo icono que custáceos |
| `frutos_de_cascara` | `Nut` | `#AE9A86` | - |
| `cacahuetes` | `Nut` | `#7B4B2A` | Mismo icono que frutos de cáscara |
| `soja` | `Bean` | `#6B7B4D` | - |
| `apio` | `Carrot` | `#16A34A` | Aproximación visual |
| `mostaza` | `CircleAlert` | `#CBAA2D` | Sin icono específico |
| `sesamo` | `Droplet` | `#A16207` | Aproximación (Aceite/Semilla) |
| `sulfitos` | `Wine` | `#7C2D3A` | - |
| `altramuces` | `Flower` | `#B98E40` | - |

#### Ejemplo de uso
```tsx
// Contiene (Fondo sólido, icono blanco)
<AllergenIconDisplay allergenId="gluten" type="contains" />

// Trazas (Fondo transparente, borde discontinuo, icono color)
<AllergenIconDisplay allergenId="gluten" type="traces" />
```

---
*Este documento esta vivo. Si se añade un nuevo patrón de diseño, debe registrarse aquí primero.*
