import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, it } from 'vitest'
import App from '../App'

// Run only with the isolated helper API and its Vite proxy; there are no mocked responses.
it('completes the corporate reference case through React and real FastAPI', async () => {
  const user = userEvent.setup()
  render(<App />)
  await user.click(await screen.findByRole('button', { name: '+ Crear primer proyecto' }))
  await user.type(screen.getByLabelText('Nombre'), 'Implementación de plataforma corporativa')
  await user.click(screen.getByRole('button', { name: 'Guardar' }))
  await screen.findByText('Aún no hay actividades')
  const rows = [
    ['Análisis', '10000000', '80', '100', '9000000'],
    ['Desarrollo', '20000000', '60', '40', '12000000'],
    ['Pruebas', '30000000', '50', '50', '16000000'],
  ]
  for (const [name, bac, planned, actual, cost] of rows) {
    await user.click(screen.getByRole('button', { name: '+ Nueva actividad' }))
    for (const [label, value] of [
      ['Nombre', name], ['Presupuesto total (BAC) COP', bac], ['Avance planificado %', planned],
      ['Avance real %', actual], ['Costo ejecutado (AC) COP', cost],
    ]) await user.type(screen.getByLabelText(label), value)
    await user.click(screen.getByRole('button', { name: 'Guardar' }))
    await screen.findByRole('rowheader', { name })
  }
  const metrics = within(screen.getByRole('region', { name: 'Indicadores consolidados' }))
  for (const value of ['$ 60.000.000,00', '$ 35.000.000,00', '$ 33.000.000,00', '$ 37.000.000,00', '$ −4.000.000,00', '$ −2.000.000,00', '0,8919', '0,9429', '$ 67.272.727,27', '$ −7.272.727,27']) {
    expect(metrics.getByText(value)).toBeInTheDocument()
  }
  expect(screen.getByRole('img', { name: /Comparación de PV/ })).toHaveTextContent('Desarrollo')
}, 30000)
